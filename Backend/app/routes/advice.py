from fastapi import APIRouter, HTTPException, Query
from ..utils.av_client import get_company_overview, get_beta, get_atr, get_sentiment, get_news
import scores_csv
import stocks

router = APIRouter()

dummy_data = [
    {
        "company": "Gamestop",
        "price": 1,
        "ticker": "GME",
        "category": "Yolo",
        "reasoning": "According to WallStreetBets, GameStop is going to the moon! Buy now!",
        "links": ["https://www.reddit.com/r/wallstreetbets/comments/167610g/most_anticipated_earning_gamestop/"],
        "risk": 100,
        "hype": 100,
        "sentiment": 75,
        "final_score": 30,
    },
    {
        "company": "Amazon",
        "price": 2.50,
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
        "price": 10,
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

@router.get("/advice")
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
        curr_res = {
            "company": company_info["Name"],
            "price": company_info[""],
            "ticker": ticker,
            "category": category,
            "reasoning": reasoning,
            "links": stocks.get_news_articles(ticker),
            "risk": scores_csv.get_risk_score_csv(ticker),
            "hype": scores_csv.get_hype_score_csv(ticker),
            "sentiment": scores_csv.get_sentiment_score_csv(ticker),
            "final_score": final_score,
        }
        res.append(curr_res.copy())

    return res