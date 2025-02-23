from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import pandas as pd
import os
import modal
import re
import json
import logging

from .scores_csv import get_sentiment_score_csv, get_hype_score_csv, get_risk_score_csv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

# Define the absolute path to the CSV file
CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    "Data",
    "reddit_stats.csv"
)
print(f"Resolved CSV Path: {CSV_PATH}")  # Debugging line
REDDIT_POSTS_SEPARATOR = ", Title: "

def read_csv_data():
    """Read and parse the CSV data"""
    if not os.path.exists(CSV_PATH):
        raise HTTPException(status_code=404, detail=f"CSV file not found at: {CSV_PATH}")
    
    df = pd.read_csv(CSV_PATH)
    df['referenced_posts'] = df['referenced_posts'].apply(lambda x: x.split(REDDIT_POSTS_SEPARATOR))
    return df

def get_ticker_data(ticker: str, df):
    """Get data for a specific ticker"""
    ticker_data = df[df['Ticker'].str.upper() == ticker.upper()]
    if ticker_data.empty:
        raise HTTPException(status_code=404, detail="Ticker not found in dataset")
    return ticker_data.iloc[0]

def parse_recommendation_response(response_text: str) -> list[dict]:
    """Robust parser for different response formats"""
    try:
        # First try direct JSON parsing
        try:
            data = json.loads(response_text)
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                return [data]
        except json.JSONDecodeError:
            pass
       # Try extracting JSON from text
        clean_text = response_text.replace('\\n', ' ').replace('\\"', "'")
        
        # Find all JSON objects/arrays in the text
        json_objects = []
        for match in re.finditer(r'\{.*?\}|\[.*?\]', clean_text, re.DOTALL):
            try:
                parsed = json.loads(match.group())
                if isinstance(parsed, list):
                    json_objects.extend(parsed)
                else:
                    json_objects.append(parsed)
            except json.JSONDecodeError:
                continue

        if not json_objects:
            raise ValueError("No valid JSON found in response text")
        # Flatten nested lists and filter for recommendation structures
        final_recommendations = []
        for obj in json_objects:
            if isinstance(obj, list):
                final_recommendations.extend(
                    [item for item in obj if isinstance(item, dict)]
                )
            elif isinstance(obj, dict) and "Ticker" in obj:
                final_recommendations.append(obj)

        if not final_recommendations:
            raise ValueError("No valid recommendations found in parsed JSON")

        return final_recommendations

    except Exception as e:
        logger.error(f"Parse Error: {str(e)} in response: {response_text}")
        raise ValueError(f"Failed to parse recommendations: {str(e)}")


class RecommendationRequest(BaseModel):
    user_prompt: str
    blacklist: list[str]
    amount: int
    user_risk: str
    yolo: int


class Advice(BaseModel):
    ticker: str
    category: str
    risk: float
    hype: float
    sentiment: float
    reasoning: str

# Get a reference to your Modal recommendation function.
try:
    modal_generate_recommendation = modal.Function.from_name("stonksensei-chat", "generate_recommendation")
except Exception as e:
    print(f"Error connecting to Modal recommendation function: {e}")
    modal_generate_recommendation = None

@router.post("/output/")
async def process_and_recommend(request: RecommendationRequest):
    """
    Reads the CSV to get the full stock list, filters out stocks in the blacklist, then
    calculates the sentiment, hype, and risk scores for each remaining stock. Finally, it
    calls the Modal-hosted generate_recommendation function with the filtered list.
    """
    if request.yolo > 6:
        request.user_risk = "High Risk, High Volatility, Short-term"

    try:
        df = read_csv_data()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    # Filter the full list based on the blacklist (case-insensitive matching on ticker)
    # Here, we assume the CSV has a column "Ticker"
    blacklist_lower = [b.lower() for b in request.blacklist]
    filtered_df = df[~df['Ticker'].str.lower().isin(blacklist_lower)]
    
    if filtered_df.empty:
        raise HTTPException(status_code=404, detail="No stocks remain after filtering by blacklist")
       # For each remaining stock, calculate the three statistics by calling the endpoints
    
    filtered_stocks = []
    for _, row in filtered_df.iterrows():
        current_ticker = row["Ticker"].upper()
        
        # Call the sentiment endpoint
        try:
            sentiment_resp = await get_sentiment_score_csv(current_ticker)
            # Expecting response like {"ticker": "...", "sentiment_score": <value>}
            sentiment_score = float(sentiment_resp.get("sentiment_score", 0))
        except Exception as e:
            sentiment_score = 0.0
        
        # Call the hype endpoint
        try:
            hype_resp = await get_hype_score_csv(current_ticker)
            hype_score = float(hype_resp.get("hype_score", 0))
        except Exception as e:
            hype_score = 0.0
        
        # Call the risk endpoint (which requires sentiment_score)
        try:
            risk_resp = await get_risk_score_csv(current_ticker, sentiment_score)
            risk_score = float(risk_resp.get("risk_score", 0))
        except Exception as e:
            print(e)
            risk_score = 0.0
        
        filtered_stocks.append({
            "ticker": current_ticker,
            "hype": round(hype_score, 2),
            "risk": round(risk_score, 2),
            "sentiment_score": round(sentiment_score, 2)
        })

    # Now, call the Modal-hosted generate_recommendation function.
    try:
        recommendation = modal_generate_recommendation.remote(request.user_prompt, filtered_stocks, request.amount, request.user_risk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling Modal recommendation function: {e}")
    
    try:
        recommendation = modal_generate_recommendation.remote(
            request.user_prompt, 
            filtered_stocks, 
            request.amount, 
            request.user_risk
        )
    except Exception as e:
        logger.error(f"Modal API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Modal API Error: {str(e)}")

    try:
        # Handle different response types
        if isinstance(recommendation, dict):
            logger.debug("Received dictionary response from Modal")
            if "recommendations" in recommendation:
                recommendations = recommendation["recommendations"]
            else:
                recommendations = [recommendation]
        elif isinstance(recommendation, str):
            logger.debug("Received string response from Modal")
            recommendations = parse_recommendation_response(recommendation)
        else:
            logger.error(f"Unexpected response type: {type(recommendation)}")
            raise ValueError(f"Unexpected response type: {type(recommendation)}")

        logger.debug(f"Parsed recommendations: {recommendations}")

        # Create score lookup and validate data
        score_lookup = {}
        for stock in filtered_stocks:
            try:
                score_lookup[stock["ticker"].upper()] = {
                    "risk": float(stock["risk"]),
                    "hype": float(stock["hype"]),
                    "sentiment": float(stock["sentiment_score"])
                }
            except KeyError as ke:
                logger.error(f"Missing key in stock data: {ke}")
                continue
            except ValueError as ve:
                logger.error(f"Invalid numeric value in stock data: {ve}")
                continue
        advice_list = []
        for rec in recommendations:
            try:
                # Validate recommendation structure
                if not all(key in rec for key in ["Ticker", "Category", "Reason"]):
                    logger.warning(f"Skipping invalid recommendation: {rec}")
                    continue

                ticker = rec["Ticker"].upper()
                stock_scores = score_lookup.get(ticker)

                if not stock_scores:
                    logger.warning(f"Skipping unknown ticker: {ticker}")
                    continue

                advice_list.append(Advice(
                    ticker=ticker,
                    category=rec["Category"],
                    risk=stock_scores["risk"],
                    hype=stock_scores["hype"],
                    sentiment=stock_scores["sentiment"],
                    reasoning=rec["Reason"]
                ))
            except Exception as e:
                logger.error(f"Error processing recommendation {rec}: {str(e)}")
                continue

        logger.info(f"Successfully processed {len(advice_list)} recommendations")
        return {"recommendations": [a.dict() for a in advice_list]}

    except Exception as e:
        logger.error(f"Final Error: {str(e)}\nFull Response: {recommendation}")
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation processing failed: {str(e)}"
        )

dummy_data = [
    {
        "company": "Gamestop",
        "price": 1,
        "ticker": "GME",
        "category": "Yolo",
        "reasoning": "According to WallStreetBets, GameStop is going to the moon! Buy now!",
        "links": ["https://www.reddit.com/r/wallstreetbets/comments/167610g/most_anticipated_earning_gamestop/"],
        "risk": 50,
        "hype": 100,
        "sentiment": 75,
        "final_score": 30,
    },
    {
        "company": "Amazon",
        "price": 250,
        "ticker": "AMZN",
        "category": "Good trade",
        "reasoning": "Amazon is doing very well right now, and congress seems to agree!",
        "links": [
            "https://www.cnn.com/markets/stocks/AMZN",
            "https://www.foxbusiness.com/politics/nancy-pelosi-sells-nvidia-apple-buys-alphabet-amazon"
        ],
        "risk": 10,
        "hype": 80,
        "sentiment": 20,
        "final_score": 80,
    },
    {
        "company": "AMD",
        "price": 100,
        "ticker": "AMD",
        "category": "Bad trade",
        "reasoning": "AMD? More like always money down. You WILL loose money by buying this.",
        "links": [],
        "risk": 100,
        "hype": 0,
        "sentiment": 50,
        "final_score": 5,
    },
]

@router.get("/fakeadvice")
async def get_advice(
    investment_amount: float = Query(..., ge=0),
    risk: str = Query(..., enum=["low", "medium", "high"]),
    timeline: str = Query(..., enum=["short", "medium", "long"]),
    yolo: int = Query(..., ge=1, le=10),
    preferences: str = Query(""),
):
    tickers = [] # Not implemented
    category = "" # Not implemented
    reasoning = "" # Not implemented
    final_score = -1 # Not implemented
    res = []
    for ticker in tickers:
        company_info = get_company_overview(ticker)
        price_info = get_price(ticker)
        curr_res = {
            "company": company_info["Name"],
            "price": price_info["05. price"],
            "ticker": ticker,
            "category": category,
            "reasoning": reasoning,
            "links": get_news_articles(ticker),
            "risk": get_risk_score_csv(ticker),
            "hype": get_hype_score_csv(ticker),
            "sentiment": get_sentiment_score_csv(ticker),
            "final_score": final_score,
        }
        res.append(curr_res.copy())

    return dummy_data
