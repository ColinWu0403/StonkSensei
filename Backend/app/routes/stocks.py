from fastapi import APIRouter, HTTPException, Query
from ..utils.av_client import get_company_overview, get_atr

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