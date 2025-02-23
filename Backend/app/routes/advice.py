from fastapi import APIRouter, HTTPException, Query
from ..utils.av_client import get_company_overview, get_beta, get_atr, get_sentiment, get_news

router = APIRouter()

dummy_data = [
    {
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
    return dummy_data