import modal
import json
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import torch.nn.functional as F

# Define the Modal App
app = modal.App(name="finbert-sentiment")

# Define the Modal Image with required dependencies
image = (
    modal.Image.debian_slim()
    .pip_install("torch", "transformers")
)

@app.function(image=image)
def analyze_sentiment(reddit_texts):
    """
    Analyzes sentiment of Reddit posts using FinBERT and returns all three sentiment scores.
    """
    # Load FinBERT model & tokenizer
    model_name = "ProsusAI/finbert"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    results = []

    for text in reddit_texts:
        # Tokenize input text
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        # Get model predictions
        with torch.no_grad():
            logits = model(**inputs).logits

        # Convert logits to probabilities
        probs = F.softmax(logits, dim=1).squeeze().tolist()

        # Create structured output
        sentiment_result = {
            "text": text,
            "negative": round(probs[0], 3),
            "neutral": round(probs[1], 3),
            "positive": round(probs[2], 3)
        }

        results.append(sentiment_result)

    # Save results to JSON
    with open("/tmp/finbert_results.json", "w") as f:
        json.dump(results, f, indent=4)

    return results

# Entry point for running the Modal App
if __name__ == "__main__":
    app.deploy("analyze_sentiment")
