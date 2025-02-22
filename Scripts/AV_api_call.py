import requests
import pandas as pd

API_KEY = "8ECXT5T3UWTOADCX"

ticker = "AAPL"

# market & sentiment analysis
# uncomment after we talk about how we want to incorporate this market & sentiment analysis data
#
# msa_url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&datatype=csv&apikey={API_KEY}'
# msa_response = requests.get(msa_url)
# with open(f'Data/{ticker}_intraday.csv', "w") as file:
#     file.write(msa_response.text)

# intraday
intraday_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&outputsize=full&interval=60min&datatype=csv&apikey={API_KEY}'
intraday_response = requests.get(intraday_url)
with open(f'Data/{ticker}_intraday.csv', "w") as file:
    file.write(intraday_response.text)
