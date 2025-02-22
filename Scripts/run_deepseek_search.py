import modal
import json

# Load the deployed function
generate_recommendation = modal.Function.from_name("stonksensei-web-search", "generate_recommendation")

# Example input data
stock_data = {"ticker": "NVDA"}  # Example stock ticker
whitelist = ["bloomberg.com", "reuters.com"]
blacklist = ["reddit.com", "twitter.com"]

# Call the deployed function asynchronously
results = generate_recommendation.remote(stock_data, whitelist, blacklist)

# Save results in a JSON file
with open("LLM_Outputs/deepseek_results.json", "w") as f:
    json.dump(results, f, indent=4)

# Print the output
print(json.dumps(results, indent=2))
