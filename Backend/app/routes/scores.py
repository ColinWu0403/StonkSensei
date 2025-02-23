# from fastapi import APIRouter, HTTPException
# from typing import List
# from ..utils.av_client import get_beta, get_atr
# from ..utils.reddit_scraper import get_reddit_engagement # doesn't exist yet
# from ..db.mongodb import database
# from models import reddit
# from bson import ObjectId
# from datetime import datetime

# import modal

# router = APIRouter()

# # Initialize Modal connection
# try:
#     analyze_sentiment = modal.Function.from_name("finbert-sentiment", "analyze_sentiment")
# except Exception as e:
#     print(f"Error connecting to Modal: {e}")
#     analyze_sentiment = None

# @router.get("/sentiment/{ticker}")
# async def get_sentiment_score(ticker: str):
#     """
#     Calculate the sentiment score for a given stock ticker.
#     """
#     try:
#         if not analyze_sentiment:
#             raise HTTPException(status_code=500, detail="Modal connection failed")
    
#         # Step 1: Get Reddit posts for the ticker
#         stock_metrics = await database["reddit"].find_one({"ticker": ticker})
#         reddit_texts = get_reddit_engagement(ticker)["posts"]
        
#         # Update database entry
#         db_reddit_stock = {
#             'ticker': ticker,
#             'mentions_count': reddit_texts["mentions"],
#             'total_upvotes': reddit_texts["upvotes"],
#             'total_comments': reddit_texts["comments"],
#             'posts_scraped': reddit_texts["total_posts"],
#             'timestamp': datetime.utcnow()
#         }
#         if stock_metrics:
#             await database["reddit"].find_one_and_update(
#                 {"ticker": ticker},
#                 {"$set": db_reddit_stock},
#                 return_document=True
#             )
#         else:
#             await database["reddit"].insert_one(db_reddit_stock)

#         # Step 2: Analyze sentiment using the deployed Modal function
#         sentiment_results = analyze_sentiment.remote(reddit_texts)
        
#         # Step 3: Calculate combined sentiment score
#         finbert_score = (
#             sentiment_results[0]["finbert"]["positive"] -
#             sentiment_results[0]["finbert"]["negative"] +
#             (sentiment_results[0]["finbert"]["neutral"] * 0.2)
#         )
#         fintwit_score = (
#             sentiment_results[0]["fintwitbert-sentiment"]["BULLISH"] -
#             sentiment_results[0]["fintwitbert-sentiment"]["BEARISH"] +
#             (sentiment_results[0]["fintwitbert-sentiment"]["NEUTRAL"] * 0.2)
#         )
#         sentiment_score = (0.7 * finbert_score) + (0.3 * fintwit_score)
        
#         return {"ticker": ticker, "sentiment_score": round(sentiment_score, 2)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/hype/{ticker}")
# async def get_hype_score(ticker: str):
#     """
#     Calculate the hype score for a given stock ticker.
#     """
#     MAX_HOUR_DIFF = 12
#     try:
#         # Step 1: Get and save Reddit engagement metrics
#         stock_metrics = await database["reddit"].find_one({"ticker": ticker})
#         engagement = None
#         if not stock_metrics or (datetime.utcnow() - stock_metrics['timestamp']).total_seconds() // 3600 > MAX_HOUR_DIFF:
#             engagement = get_reddit_engagement(ticker)
#             db_reddit_stock = {
#                 'ticker': ticker,
#                 'mentions_count': engagement["mentions"],
#                 'total_upvotes': engagement["upvotes"],
#                 'total_comments': engagement["comments"],
#                 'posts_scraped': engagement["total_posts"],
#                 'timestamp': datetime.utcnow()
#             }

#             if not stock_metrics:
#                 await database["reddit"].insert_one(db_reddit_stock)
#             else:
#                 await database["reddit"].find_one_and_update(
#                     {"ticker": ticker},
#                     {"$set": db_reddit_stock},
#                     return_document=True
#                 )
#         else:
#             engagement = {
#                 "mentions": stock_metrics["mentions_count"],
#                 "upvotes": stock_metrics["total_upvotes"],
#                 "comments": stock_metrics["total_comments"],
#                 "total_posts": stock_metrics["posts_scraped"],
#             }
        
#         # Step 2: Calculate hype score
#         mentions = engagement["mentions"]
#         upvotes = engagement["upvotes"]
#         comments = engagement["comments"]
#         total_posts = engagement["total_posts"]
        
#         hype_score = (mentions + (upvotes * 0.5) + (comments * 0.3)) / total_posts
        
#         return {"ticker": ticker, "hype_score": round(hype_score, 2)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/risk/{ticker}")
# async def get_risk_score(ticker: str):
#     """
#     Calculate the risk score for a given stock ticker.
#     """
#     try:
#         # Step 1: Get Beta and ATR from AlphaVantage
#         beta = float(get_beta(ticker))
#         atr = float(get_atr(ticker, interval="monthly", time_period=60)["Technical Analysis: ATR"]["2023-10-31"]["ATR"])
        
#         # Step 2: Get sentiment variability (standard deviation of sentiment scores over time)
#         sentiment_variability = 2.5  # Placeholder (calculate from historical data)
        
#         # Step 3: Calculate risk score
#         risk_score = (beta * 0.5) + (atr * 10) + (sentiment_variability * 5)
        
#         return {"ticker": ticker, "risk_score": round(risk_score, 2)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))