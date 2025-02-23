import pandas as pd
import re
from collections import defaultdict
import os

# Dictionary to map company names to tickers
company_to_ticker = {
    # Tickers and company names
    "aapl": "AAPL",  # Apple
    "tsla": "TSLA",  # Tesla
    "amzn": "AMZN",  # Amazon
    "gme": "GME",    # GameStop
    "msft": "MSFT",  # Microsoft
    "amc": "AMC",    # AMC Entertainment
    "bb": "BB",      # BlackBerry
    "nok": "NOK",    # Nokia
    "googl": "GOOGL",# Alphabet (Google)
    "fb": "FB",      # Facebook (Meta)
    "nvda": "NVDA",  # NVIDIA
    "spy": "SPY",    # SPDR S&P 500 ETF
    "qqq": "QQQ",    # Invesco QQQ ETF
    "tsmc": "TSMC",  # Taiwan Semiconductor Manufacturing Company
    "amd": "AMD",    # Advanced Micro Devices
    "djt": "DJT",    # Trump Media & Technology Group
    "pltr": "PLTR",  # Palantir

    # Common company names (optional additions)
    "apple": "AAPL",
    "tesla": "TSLA",
    "amazon": "AMZN",
    "gamestop": "GME",
    "microsoft": "MSFT",
    "nvidia": "NVDA",
    "costco": "COST",
    "taiwan semiconductor": "TSMC",
    "advanced micro devices": "AMD",
    "palantir": "PLTR",
    "blackberry": "BB",
    "nokia": "NOK",
    "google": "GOOGL",
    "facebook": "FB",
    "meta": "FB",  # Facebook's parent company
    "trump media": "DJT",
    "jpmorgan chase": "JPM",
    "bank of america": "BAC",
    "goldman sachs": "GS",
    "comcast": "CMCSA",
    "union pacific": "UNP",
    "nike": "NKE",
    "pnc financial": "PNC",
    "colgate-palmolive": "CL",
    "3m": "MMM",
    "air products and chemicals": "APD",
    "norfolk southern": "NSC",
    "metlife": "MET",
    "schlumberger": "SLB",
    "sempra": "SRE",
    "phillips 66": "PSX",
    "diamondback energy": "FANG",
    "marathon petroleum": "MPC",
    "newmont": "NEM",
    "public service enterprise group": "PEG",
    "keurig dr pepper": "KDP",
    "valero energy": "VLO",
    "sysco": "SYY",
    "entergy": "ETR",
    "ppg industries": "PPG",
    "halliburton": "HAL",
    "devon energy": "DVN",
    "cms energy": "CMS",
    "coterra energy": "CTRA",
    "corebridge financial": "CRBG",
    "cf industries": "CF",
    "equitable holdings": "EQH",
    "east west bancorp": "EWBC",
    "tapestry": "TPR",
    "permian resources": "PR",
    "tko group": "TKO",
    "first horizon": "FHN",
    "ovintiv": "OVV",
    "webster financial": "WBS",
    "bath & body works": "BBWI",
    "chord energy": "CHRD",
    "americold realty trust": "COLD",
    "california resources": "CRC",
    "six flags entertainment": "FUN",
    "northern oil and gas": "NOG",
    "travel + leisure": "TNL",
    "patterson-uti energy": "PTEN",
    "banc of california": "BANC",
    "netstreit": "NTST",
    "berkshire": "BRK",
    "moderna": "MRNA",
    "carlisle": "CSL",
    "intuitive": "LUNR",
    "barclays": "VXX",
    "dropbox": "DBX",
    "hims & hers health": "HIMS",
    "unitedhealth": "UNH",
    "archer aviation": "ACHR"
}

# Function to extract tickers and company names from text
def extract_tickers_and_names(text):
    # Regex to match uppercase words with 1-5 letters (tickers)
    tickers = re.findall(r'\b[A-Z]{1,5}\b', text)
    # Regex to match company names (case-insensitive)
    names = re.findall(r'\b(?:' + '|'.join(company_to_ticker.keys()) + r')\b', text.lower())
    return tickers + names

# Function to clean and filter tickers
def clean_tickers(text):
    if not isinstance(text, str):  # Handle NaN or non-string values
        return []
    potential_tickers_and_names = extract_tickers_and_names(text)
    # Convert company names to tickers and filter valid tickers
    cleaned_tickers = []
    for item in potential_tickers_and_names:
        if item.lower() in company_to_ticker:  # Convert company name to ticker
            cleaned_tickers.append(company_to_ticker[item.lower()])
    return list(set(cleaned_tickers))  # Remove duplicates

# Function to truncate the body text
def truncate_body(body, max_length=100):
    if not isinstance(body, str):  # Handle NaN or non-string values
        return ""
    if len(body) > max_length:
        return body[:max_length] + "..."
    return body

# Function to process a row (title and body)
def process_row(row):
    title_tickers = clean_tickers(row["title"])
    body_tickers = clean_tickers(str(row["body"]))
    return list(set(title_tickers + body_tickers))  # Combine and remove duplicates

# Load the CSV file
input_csv = "../Data/scrape_hot.csv"
output_csv = "../Data/reddit_stats.csv"

# Read the CSV into a DataFrame
df = pd.read_csv(input_csv)

# Clean the upvotes column
df["upvotes"] = df["upvotes"].astype(str)  # Ensure it's a string
df["upvotes"] = df["upvotes"].str.replace('"', '')  # Remove quotes
df["upvotes"] = df["upvotes"].str.replace(',', '')  # Remove commas
df["upvotes"] = pd.to_numeric(df["upvotes"], errors="coerce")  # Convert to numeric

# Convert num_comments to integers (handle errors by coercing to NaN)
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

# Fill NaN values with 0 (if any)
df["upvotes"] = df["upvotes"].fillna(0).astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

# Initialize a dictionary to store statistics
ticker_stats = defaultdict(lambda: {"total_upvotes": 0, "total_comments": 0, "num_of_mentions": 0, "referenced_posts": ""})

# Process each row and update statistics
for _, row in df.iterrows():
    tickers = process_row(row)
    for ticker in tickers:
        ticker_stats[ticker]["total_upvotes"] += row["upvotes"]
        ticker_stats[ticker]["total_comments"] += row["num_comments"]
        ticker_stats[ticker]["num_of_mentions"] += 1
        # Add the post title and truncated body to referenced_posts
        post_reference = f"Title: {row['title']}\nBody: {truncate_body(str(row['body']))}"
        if ticker_stats[ticker]["referenced_posts"]:  # If not empty, add a separator
            ticker_stats[ticker]["referenced_posts"] += ", "
        ticker_stats[ticker]["referenced_posts"] += post_reference

# Convert the dictionary to a DataFrame
new_stats_df = pd.DataFrame.from_dict(ticker_stats, orient="index").reset_index()
new_stats_df.columns = ["Ticker", "total_upvotes", "total_comments", "num_of_mentions", "referenced_posts"]

# Check if the output CSV already exists
if os.path.exists(output_csv):
    # Load the existing data
    existing_stats_df = pd.read_csv(output_csv)
    # Combine the new data with the existing data
    combined_stats_df = pd.concat([existing_stats_df, new_stats_df])
    # Group by Ticker and aggregate the metrics
    combined_stats_df = combined_stats_df.groupby("Ticker", as_index=False).agg({
        "total_upvotes": "sum",
        "total_comments": "sum",
        "num_of_mentions": "sum",
        "referenced_posts": lambda x: ", ".join(x)
    })
else:
    # If the file doesn't exist, use the new data
    combined_stats_df = new_stats_df

# Save the combined results to the CSV
combined_stats_df.to_csv(output_csv, index=False)

print(f"Processed data saved to {output_csv}")