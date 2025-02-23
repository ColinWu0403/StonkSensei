import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

def get_company_overview(ticker: str):
    """
    Get company overview data from AlphaVantage.
    """
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    data = response.json()
    return data

def get_beta(ticker: str):
    """
    Get beta from AlphaVantage.
    """
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    data = response.json()
    # only return beta value
    return {"beta": data.get("Beta")}

def get_atr(ticker: str, interval: str = "monthly", time_period: int = 60):
    """
    Get Average True Range (ATR) data from AlphaVantage.
    """
    url = f"https://www.alphavantage.co/query?function=ATR&symbol={ticker}&interval={interval}&time_period={time_period}&apikey={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    data = response.json()
    # only return last month's averaged ATR
    last_refeshed_date = data["Meta Data"]["3: Last Refreshed"]
    atr_value = data["Technical Analysis: ATR"][last_refeshed_date]["ATR"]
    return {"atr": atr_value}
    

def get_sentiment(ticker: str, num_articles: int):
    """
    Get Market Sentiment data from AlphaVantage.
    """
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&limit={num_articles}&datatype=json&apikey={API_KEY}'
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    data = response.json()

    # get average sentiment score (sum of all sentiment scores times relevance scores / number of articles)
    num_articles = int(data["items"])
    articles = data["feed"]

    summation = 0.0
    for article in articles:
        for ticker_scores in article["ticker_sentiment"]:
            if ticker_scores["ticker"] == ticker:
                relevance = float(ticker_scores["relevance_score"])
                sentiment = float(ticker_scores["ticker_sentiment_score"])
                summation += relevance * sentiment

    avg_sentiment = summation / num_articles
    
    return {"sentiment": avg_sentiment}


def get_news(ticker: str, num_articles: int):
    """
    Get Market News data from AlphaVantage.
    """
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&limit={num_articles}&datatype=json&apikey={API_KEY}'
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    data = response.json()
    return data.get("feed") # only return news articles

def get_price(ticker: str):
    """
    Get stock price
    """
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data