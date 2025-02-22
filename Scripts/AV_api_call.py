import requests
import pandas as pd

API_KEY = "8ECXT5T3UWTOADCX"

# market & sentiment analysis
msa_url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey={API_KEY}'
msa_request = requests.get(msa_url)
msa_data = msa_request.json()
msa_df = pd.dataFrame(msa_data['changeme!!!!!!!!!!!!!!!!'])
msa_df.to_csv()

print(msa_data)

intraday_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&outputsize=full&interval=60min&apikey={API_KEY}'
intraday_request = requests.get(intraday_url)
intraday_data = intraday_request.json()
intraday_df = pd.dataFrame(intraday_data['changeme!!!!!!!!!!!!!!!!'])
intraday_df.to_csv()

print(intraday_data)

