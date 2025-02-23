from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import stocks, sentiment, scores_csv

app = FastAPI(title="Stonk Sensei Backend", version="0.1.0")

# CORS setup (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
app.include_router(sentiment.router, prefix="/sentiment", tags=["sentiment"])
app.include_router(scores_csv.router, prefix="/scores", tags=["scores"])

@app.get("/")
async def root():
    return {"message": "Stock Analysis API - See /docs for documentation"}