import modal
import json
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import torch.nn.functional as F

app = modal.App(name="finbert-sentiment")

image = (
    modal.Image.debian_slim()
    .pip_install("torch", "transformers")
)

@app.function(image=image)
def analyze_sentiment(reddit_texts):
    # Load both models and tokenizers
    finbert_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    finbert_tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    
    # Corrected FinTwitBERT model with sentiment labels
    fintwit_model = AutoModelForSequenceClassification.from_pretrained("StephanAkkerman/FinTwitBERT-sentiment")
    fintwit_tokenizer = AutoTokenizer.from_pretrained("StephanAkkerman/FinTwitBERT-sentiment")

    # Get label mappings from both models
    finbert_labels = finbert_model.config.id2label
    fintwit_labels = fintwit_model.config.id2label  # Now returns 3 proper labels

    results = []

    for text in reddit_texts:
        # Process with FinBERT
        finbert_inputs = finbert_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            finbert_logits = finbert_model(**finbert_inputs).logits
        finbert_probs = F.softmax(finbert_logits, dim=1).squeeze()

        # Process with FinTwitBERT-sentiment
        fintwit_inputs = fintwit_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            fintwit_logits = fintwit_model(**fintwit_inputs).logits
        fintwit_probs = F.softmax(fintwit_logits, dim=1).squeeze()

        # Map probabilities using each model's label config
        results.append({
            "text": text,
            "finbert": {
                finbert_labels[i]: round(prob.item(), 3)
                for i, prob in enumerate(finbert_probs)
            },
            "fintwitbert-sentiment": {
                fintwit_labels[i]: round(prob.item(), 3)
                for i, prob in enumerate(fintwit_probs)
            }
        })

    with open("/tmp/sentiment_results.json", "w") as f:
        json.dump(results, f, indent=4)

    return results

if __name__ == "__main__":
    app.deploy("analyze_sentiment")