from fastapi import APIRouter, HTTPException
from typing import List
import modal

router = APIRouter()

# Initialize Modal connection
try:
    analyze_sentiment = modal.Function.from_name("finbert-sentiment", "analyze_sentiment")
except Exception as e:
    print(f"Error connecting to Modal: {e}")
    analyze_sentiment = None

@router.post("/analyze")
async def analyze_text_sentiment(texts: List[str]):
    if not analyze_sentiment:
        raise HTTPException(status_code=500, detail="Modal connection failed")
    
    try:
        results = analyze_sentiment.remote(texts)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))