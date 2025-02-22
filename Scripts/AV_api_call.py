import requests
import pandas as pd
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

tickers = ["AAPL"]

# market & sentiment analysis

for ticker in tickers:
    msa_url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&limit=1000&datatype=json&apikey={API_KEY}'
    msa_response = requests.get(msa_url)
    msa_json = msa_response.json()

    with open(f'Data/{ticker}_seniments.json', "w") as file:
        json.dump(msa_json, file, indent=4)

# fundamental data api -- company overview (gets data containing beta)
# for ticker in tickers:
#     beta_url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=demo{API_KEY}'
#     beta_response = requests.get(beta_url)
#     beta_json = beta_response.json()

#     print(beta_json)
#     with open(f'Data/{ticker}_fundamental_data.json', "w") as file:
#         json.dump(beta_json, file, indent=4)

# technical indicators api -- ATR (gets ATR--average true range)
# for ticker in tickers:
#     atr_url = f'https://www.alphavantage.co/query?function=ATR&symbol={ticker}&interval=monthly&time_period=60&apikey=demo{API_KEY}'
#     atr_response = requests.get(atr_url)
#     atr_json = atr_response.json()

#     print(atr_json)
#     with open(f'Data/{ticker}_ATR.json', "w") as file:
#         json.dump(atr_json, file, indent=4)