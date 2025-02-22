import modal

# Load the deployed function
analyze_sentiment = modal.Function.from_name("finbert-sentiment", "analyze_sentiment")

# Example Reddit posts
reddit_texts = [
    "GME is gonna skyrocket 🚀🚀",
    "I think TSLA is overvalued, sell now!",
    "AAPL might be a solid long-term hold.",
    "Advanced Money Destroyer just won’t go up. I’ve put All My Dollars in this stock and what do I get? Account Massively Drained. I was told stocks only go up and that some good DD prevents the inevitable Wendy’s dumpster but I just Ain’t Making Dollars. I mean, it Ain’t Making Dividends, it’s Always Moving Down, and just had Another Massive Dip.",
    "Adding to the recent million capital raise, ACHR now has about $1 billion in liquidity, giving them a solid runway to keep innovating without the worry of near-term funding. This move not only strengthens their balance sheet but also reduces the risk of future stock dilution, which has been a concern for the major investors for a while now.",
    "I've held this in long enough. The shame, guilt, lies. Pretending to be cool and knowing what the fuck I'm talking about. I've been holding this in for years. I've cried and cried and cried. I'm fed up with my bitch behavior. It's time to fucking take things into my own hands and change. I'm not stopping, I'm going to gain this all back the slow, and right way. Here's my story."
]

# Call the hosted FinBERT model
results = analyze_sentiment.call(reddit_texts)

# Print results
print(results)
