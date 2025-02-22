import modal
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = modal.App(name="stonksensei-core")
image = modal.Image.debian_slim().pip_install(
    "torch", 
    "transformers",
    "accelerate"
)

MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        load_in_8bit=True,
        torch_dtype=torch.bfloat16
    )
    return tokenizer, model

@app.function(image=image, gpu="A100")
def generate_recommendation(user_prompt: str, stock_data: dict, whitelist: list, blacklist: list):
    tokenizer, model = load_model()
    
    category = categorize_stock(stock_data, blacklist)
    
    system_prompt = f"""You are StonkSensei, a financial AI assistant. Analyze stocks based on:
- Risk Score: {stock_data['risk']} ({get_risk_level(stock_data['risk'])})
- Sentiment Score: {stock_data['sentiment']}/10
- Hype Score: {stock_data['hype']}/10
- Category: {category}

Decision Rules:
{decision_tree_rules()}

User Preferences:
- Whitelist: {', '.join(whitelist)}
- Blacklist: {', '.join(blacklist)}
- Prompt: {user_prompt}"""

    inputs = tokenizer.apply_chat_template(
        [{"role": "system", "content": system_prompt}],
        return_tensors="pt"
    ).to(model.device)
    
    outputs = model.generate(
        inputs,
        max_new_tokens=512,
        temperature=0.7,
        do_sample=True
    )
    
    return format_output(
        stock_data,
        category,
        tokenizer.decode(outputs[0], skip_special_tokens=True)
    )

def format_output(stock_data, category, analysis):
    return {
        "ticker": stock_data["ticker"],
        "category": category,
        "analysis": clean_response(analysis),
        "metrics": stock_data
    }

def categorize_stock(stock_data: dict, blacklist: list) -> str:
    """Apply decision tree categorization based on stock data and blacklist."""
    ticker = stock_data["ticker"]
    if ticker in blacklist:
        return "❌ Avoid (Blacklisted)"
    
    risk = stock_data["risk"]
    sentiment = stock_data["sentiment"]
    hype = stock_data["hype"]
    
    risk_level = get_risk_level(risk)
    sentiment_level = "High" if sentiment >= 7 else "Low" if sentiment < 4 else "Medium"
    hype_level = "High" if hype >= 6 else "Low" if hype < 3 else "Medium"
    
    # Decision tree implementation
    if risk_level == "Low":
        if sentiment_level == "High" and hype_level == "High":
            return "✅ Strong Buy"
        elif hype_level == "High":
            return "❌ Avoid"
    elif risk_level == "Medium":
        if sentiment_level == "High" and hype_level == "Medium":
            return "✅ Consider Buying"
    elif risk_level == "High":
        if sentiment_level == "High" and hype_level == "High":
            return "⚠️ YOLO Pick"
        elif sentiment_level == "Low" and hype_level == "Low":
            return "❌ Avoid"
    
    return "⚠️ Neutral (Further Analysis Needed)"

def get_risk_level(risk_score: float) -> str:
    if risk_score < 30:
        return "Low"
    elif 30 <= risk_score <= 60:
        return "Medium"
    else:
        return "High"

def decision_tree_rules() -> str:
    return """Decision Tree:
            Low Risk + High Sentiment + High Hype → ✅ Strong Buy
            Low Risk + Low Sentiment + High Hype → ❌ Avoid
            Medium Risk + High Sentiment + Medium Hype → ✅ Consider Buying
            High Risk + High Sentiment + High Hype → ⚠️ YOLO Pick
            High Risk + Low Sentiment + Low Hype → ❌ Avoid"""

def clean_response(text: str) -> str:
    """Clean up LLM output by removing system tokens if any."""
    # This example assumes a token like '[/INST]' might be in the output.
    return text.split("[/INST]")[-1].strip()

# Example usage remains the same
if __name__ == "__main__":
    stock_data_example = {
        "ticker": "AAPL",
        "risk": 25,
        "sentiment": 8.2,
        "hype": 6.5
    }
    
    result = generate_recommendation.remote(
        user_prompt="Should I invest in AAPL for long-term growth?",
        stock_data=stock_data_example,
        whitelist=["AAPL", "MSFT"],
        blacklist=["TSLA"]
    )
    print(result)