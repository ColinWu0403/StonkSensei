from fastapi import APIRouter, HTTPException
from typing import List
from ..utils.av_client import get_beta, get_atr
from ..utils.reddit_scraper import get_reddit_engagement # doesn't exist yet

import modal

router = APIRouter()

# Initialize Modal connection
try:
    analyze_sentiment = modal.Function.from_name("finbert-sentiment", "analyze_sentiment")
except Exception as e:
    print(f"Error connecting to Modal: {e}")
    analyze_sentiment = None

@router.get("/sentiment/{ticker}")
async def get_sentiment_score(ticker: str):
    """
    Calculate the sentiment score for a given stock ticker.
    """
    try:
        if not analyze_sentiment:
            raise HTTPException(status_code=500, detail="Modal connection failed")
    
        # Step 1: Get Reddit posts for the ticker
        reddit_texts = get_reddit_engagement(ticker)["posts"]
        
        # Step 2: Analyze sentiment using the deployed Modal function
        sentiment_results = analyze_sentiment.remote(reddit_texts)
        
        # Step 3: Calculate combined sentiment score
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
        
        return {"ticker": ticker, "sentiment_score": round(sentiment_score, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hype/{ticker}")
async def get_hype_score(ticker: str):
    """
    Calculate the hype score for a given stock ticker.
    """
    try:
        # Step 1: Get Reddit engagement metrics
        engagement = get_reddit_engagement(ticker)
        
        # Step 2: Calculate hype score
        mentions = engagement["mentions"]
        upvotes = engagement["upvotes"]
        comments = engagement["comments"]
        total_posts = engagement["total_posts"]
        
        hype_score = (mentions + (upvotes * 0.5) + (comments * 0.3)) / total_posts
        
        return {"ticker": ticker, "hype_score": round(hype_score, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/risk/{ticker}")
async def get_risk_score(ticker: str):
    """
    Calculate the risk score for a given stock ticker.
    """
    try:
        # Step 1: Get Beta and ATR from AlphaVantage
        beta = float(get_beta(ticker))
        atr = float(get_atr(ticker, interval="monthly", time_period=60)["Technical Analysis: ATR"]["2023-10-31"]["ATR"])
        
        # Step 2: Get sentiment variability (standard deviation of sentiment scores over time)
        sentiment_variability = 2.5  # Placeholder (calculate from historical data)
        
        # Step 3: Calculate risk score
        risk_score = (beta * 0.5) + (atr * 10) + (sentiment_variability * 5)
        
        return {"ticker": ticker, "risk_score": round(risk_score, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))