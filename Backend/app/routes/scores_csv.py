from fastapi import APIRouter, HTTPException
import pandas as pd
import os
import modal

router = APIRouter()

# Initialize Modal connection
try:
    analyze_sentiment = modal.Function.from_name("finbert-sentiment", "analyze_sentiment")
except Exception as e:
    print(f"Error connecting to Modal: {e}")
    analyze_sentiment = None

# Get the absolute path to the CSV file
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
    ticker_data = df[df['Ticker'] == ticker]
    if ticker_data.empty:
        raise HTTPException(status_code=404, detail="Ticker not found in dataset")
    return ticker_data.iloc[0]

@router.get("/sentiment-csv/{ticker}")
async def get_sentiment_score_csv(ticker: str):
    """Calculate sentiment score from CSV data"""
    try:
        df = read_csv_data()
        ticker_data = get_ticker_data(ticker, df)
        
        # Extract post texts from referenced_posts
        posts = []
        for post in ticker_data['referenced_posts']:
            if isinstance(post, str) and "Body: " in post:
                body = post.split("Body: ")[-1]
                posts.append(body)
        
        sentiment_results = analyze_sentiment.remote(posts)
        
        finbert_score = (
            sentiment_results[0]["finbert"]["positive"] -
            sentiment_results[0]["finbert"]["negative"] +
            (sentiment_results[0]["finbert"]["neutral"] * 0.2)
        )
        fintwit_score = (
            sentiment_results[0]["fintwitbert-sentiment"]["BULLISH"] -
            sentiment_results[0]["fintwitbert-sentiment"]["BEARISH"] +
            (sentiment_results[0]["fintwitbert-sentiment"]["NEUTRAL"] * 0.2)
        )
        sentiment_score = (0.7 * finbert_score) + (0.3 * fintwit_score)
        
        return {"ticker": ticker, "sentiment_score": sentiment_score}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hype-csv/{ticker}")
async def get_hype_score_csv(ticker: str):
    """Calculate hype score from CSV data"""
    try:
        df = read_csv_data()
        ticker_data = get_ticker_data(ticker, df)
        
        # Calculate hype score using CSV columns
        mentions = ticker_data['num_of_mentions']
        upvotes = ticker_data['total_upvotes']
        comments = ticker_data['total_comments']
        
        # Adjusted formula using available CSV data
        hype_score = (mentions + (upvotes * 0.5) + (comments * 0.3)) / max(mentions, 1)
        
        return {"ticker": ticker, "hype_score": round(hype_score, 2)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/risk-csv/{ticker}")
async def get_risk_score_csv(ticker: str):
    """Calculate risk score (combination of volatility and sentiment)"""
    try:
        df = read_csv_data()
        ticker_data = get_ticker_data(ticker, df)
        
        # Get volatility metrics (you'll need to implement these)
        beta = 1.2  # Placeholder - implement actual beta calculation
        atr = 5.67  # Placeholder - implement actual ATR calculation
        
        # Get sentiment variability from CSV history
        sentiment_variability = 2.5  # Placeholder
        
        risk_score = (beta * 0.5) + (atr * 10) + (sentiment_variability * 5)
        
        return {"ticker": ticker, "risk_score": round(risk_score, 2)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))