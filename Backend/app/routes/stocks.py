from fastapi import APIRouter, HTTPException, Query
from ..utils.av_client import get_company_overview, get_atr, get_sentiment, get_news

router = APIRouter()

@router.get("/{ticker}/overview")
async def get_stock_overview(ticker: str):
    """
    Get company overview data for a given ticker.
    """
    try:
        return get_company_overview(ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{ticker}/atr")
async def get_average_true_range(
    ticker: str,
    interval: str = Query("monthly", enum=["daily", "weekly", "monthly"]),
    time_period: int = Query(60, ge=1)
):
    """
    Get Average True Range (ATR) data for a given ticker.
    """
    try:
        return get_atr(ticker, interval, time_period)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{ticker}/sentiment")
async def get_market_sentiment(
    ticker: str, 
    num_articles: int = Query(1000, ge=1)
):
    """
    Get Market Sentiment data for a given ticker.
    """
    try:
        return get_sentiment(ticker, num_articles)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{ticker}/news")
async def get_news_articles(
    ticker: str,
    num_articles: int = Query(5, ge=1)
):
    """
    Get Market News data for a given ticker.
    """
    try:
        return get_news(ticker, num_articles)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))