import modal
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import requests
from bs4 import BeautifulSoup

app = modal.App(name="stonksensei-web-aware")
image = modal.Image.debian_slim().pip_install(
    "torch", "transformers", "accelerate", "requests", "beautifulsoup4"
)

# Model configuration
SMALL_MODEL = "deepseek-ai/deepseek-moe-16b-chat"
LARGE_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"

def load_models():
    """Load both models with different quantization strategies"""
    small_tokenizer = AutoTokenizer.from_pretrained(SMALL_MODEL)
    small_model = AutoModelForCausalLM.from_pretrained(
        SMALL_MODEL,
        device_map="auto",
        load_in_4bit=True,
        torch_dtype=torch.bfloat16
    )
    
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
    # Load models
    (small_tok, small_model), (large_tok, large_model) = load_models()
    
    # 1. Search with Deepseek ------------------------------------------------------
    search_prompt = f"""Search the internet and find 3 precise, recent, and credible news articles 
                  about {stock_data['ticker']} stock from financial websites. Focus on:
                  - Market trends
                  - Earnings reports
                  - Analyst opinions
                  - Regulatory changes
                  Timeframe: Last 7 days"""
    
    search_inputs = small_tok(search_prompt, return_tensors="pt").to(small_model.device)
    search_output = small_model.generate(
        search_inputs,
        max_new_tokens=150,
        temperature=0.4
    )
    queries = small_tok.decode(search_output[0], skip_special_tokens=True).split("\n")
    
    # 2. Generate analysis with your original system prompt ----------------------------
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
                  - Prompt: {user_prompt}

                  Recent News Context:
                  {format_articles(articles)}"""

    analysis_inputs = large_tok.apply_chat_template(
        [{"role": "system", "content": system_prompt}],
        return_tensors="pt"
    ).to(large_model.device)
    
    analysis_output = large_model.generate(
        analysis_inputs,
        max_new_tokens=512,
        temperature=0.7
    )
    
    return format_final_output(
        stock_data,
        large_tok.decode(analysis_output[0], skip_special_tokens=True),
        articles,
        category
    )

def google_search(query: str):
    """Simulate Google search using Serper API (replace with actual API call)"""
    # For real implementation, use:
    # https://serper.dev or https://newsapi.org
    return [
        {
            "title": f"News about {query}",
            "link": "https://example.com/article1",
            "snippet": "Sample article content about the stock..."
        }
    ]

def process_search_results(results):
    """Process and clean search results"""
    return [{
        "title": r.get("title", ""),
        "url": r.get("link", ""),
        "summary": extract_key_info(r.get("snippet", ""))
    } for r in results]

def extract_key_info(text: str):
    """Use simple NLP to extract key financial info"""
    return text[:250] + "..."  # Simple truncation for demo

def format_articles(articles):
    return "\n".join([f"• {a['title']}: {a['summary']}" for a in articles])

def format_final_output(stock_data, analysis, articles, category):
    return {
        "ticker": stock_data["ticker"],
        "category": category,
        "analysis": clean_analysis(analysis),
        "news": articles,
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
