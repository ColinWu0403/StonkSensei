import modal
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Define the Modal App
app = modal.App(name="stonksensei-recommender")

image = modal.Image.debian_slim().pip_install(
    "torch", 
    "transformers",
    "accelerate",
    "bitsandbytes"  # For 4-bit quantization
)

# Model configuration
SMALL_MODEL = "deepseek-ai/deepseek-moe-16b-chat"  # Efficient for search
LARGE_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"  # Powerful for analysis

def load_models():
    """Load both models with different quantization strategies"""
    # Small model - 4-bit quantized for efficiency
    small_tokenizer = AutoTokenizer.from_pretrained(SMALL_MODEL)
    small_model = AutoModelForCausalLM.from_pretrained(
        SMALL_MODEL,
        device_map="auto",
        load_in_4bit=True,
        torch_dtype=torch.bfloat16
    )
    
    # Large model - 8-bit quantized for balance
    large_tokenizer = AutoTokenizer.from_pretrained(LARGE_MODEL)
    large_model = AutoModelForCausalLM.from_pretrained(
        LARGE_MODEL,
        device_map="auto",
        load_in_8bit=True,
        torch_dtype=torch.bfloat16
    )
    
    return (small_tokenizer, small_model), (large_tokenizer, large_model)

@app.function(image=image, gpu="A100", timeout=300)
def generate_recommendation(user_prompt: str, stock_data: dict, whitelist: list, blacklist: list):
    # Load both models
    (small_tok, small_model), (large_tok, large_model) = load_models()
    
    # 1. News search with small model --------------------------------------------------
    news_prompt = f"""Generate search queries to find recent news about {stock_data['ticker']} stock. 
    Focus on: market trends, earnings reports, and analyst opinions from the last week."""
    
    news_inputs = small_tok(news_prompt, return_tensors="pt").to(small_model.device)
    news_queries = small_model.generate(
        news_inputs,
        max_new_tokens=100,
        temperature=0.3
    )
    decoded_queries = small_tok.decode(news_queries[0], skip_special_tokens=True)
    
    # 2. Get news results (simulated) --------------------------------------------------
    news_results = simulate_news_search(decoded_queries)  # Replace with real API calls
    
    # 3. Main analysis with large model ------------------------------------------------
    analysis_prompt = f"""Analyze {stock_data['ticker']} stock considering:
    - User question: {user_prompt}
    - Key metrics: {stock_data}
    - Recent news: {news_results}
    - Whitelist/Blacklist: {whitelist}/{blacklist}
    
    Provide detailed analysis with recommendations."""
    
    analysis_inputs = large_tok(analysis_prompt, return_tensors="pt").to(large_model.device)
    analysis_output = large_model.generate(
        analysis_inputs,
        max_new_tokens=512,
        temperature=0.7
    )
    
    return format_output(
        stock_data, 
        large_tok.decode(analysis_output[0], skip_special_tokens=True),
        news_results
    )

def simulate_news_search(queries: str):
    """Replace this with actual news API calls using the generated queries"""
    return [
        {"source": "Bloomberg", "summary": "Company announces record earnings"},
        {"source": "WSJ", "summary": "New product launch delayed"}
    ]

def format_output(stock_data: dict, analysis: str, news: list):
    return {
        "ticker": stock_data["ticker"],
        "category": categorize_stock(stock_data, []),
        "analysis": clean_analysis(analysis),
        "news": news,
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

# Example usage for local testing (will run on Modal when deployed)
if __name__ == "__main__":
    stock_data_example = {
        "ticker": "AAPL",
        "risk": 25,
        "sentiment": 8.2,
        "hype": 6.5
    }
    
    user_prompt_example = "Should I invest in AAPL for long-term growth?"
    
    result = generate_recommendation.remote(
        user_prompt=user_prompt_example,
        stock_data=stock_data_example,
        whitelist=["AAPL", "MSFT"],
        blacklist=["TSLA"]
    )
    
    print(result)
