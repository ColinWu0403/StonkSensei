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
    return response.json()

def get_atr(ticker: str, interval: str = "monthly", time_period: int = 60):
    """
    Get Average True Range (ATR) data from AlphaVantage.
    """
    url = f"https://www.alphavantage.co/query?function=ATR&symbol={ticker}&interval={interval}&time_period={time_period}&apikey={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    return response.json()

def get_sentiment(ticker: str, num_articles: int):
    """
    Get Market Sentiment data from AlphaVantage.
    """
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&limit={num_articles}&datatype=json&apikey={API_KEY}'
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    data = response.json()
    data.pop("feed", None) # only return sentiment data
    return data

def get_news(ticker: str, num_articles: int):
    """
    Get Market News data from AlphaVantage.
    """
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&limit={num_articles}&datatype=json&apikey={API_KEY}'
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    data = response.json()
    return data.get("feed") # only return news articles