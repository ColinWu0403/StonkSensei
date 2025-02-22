import modal
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import json
from pathlib import Path

app = modal.App(name="stonksensei-chat")

# Create a persistent Volume for caching model shards
volume = modal.Volume.from_name("deepseek-cache", create_if_missing=True)

image = modal.Image.debian_slim().pip_install(
    "torch", 
    "transformers",
    "accelerate",
    "bitsandbytes"
)

# Directory where the model will be cached
CACHE_DIR = Path("/cache")

# Model configuration
MODEL_NAME = "deepseek-ai/deepseek-moe-16b-chat"

def load_model():
    """Load the small DeepSeek model with 4-bit quantization and trust_remote_code"""
    # Configure 4-bit quantization
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR, local_files_only=False)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        quantization_config=quantization_config,
        trust_remote_code=True,
        cache_dir=CACHE_DIR,
        local_files_only=False
    )
    return tokenizer, model

@app.function(image=image, gpu="h100", volumes={CACHE_DIR: volume}, timeout=1800)
def generate_recommendation(user_prompt: str, stock_data: list, whitelist: list, blacklist: list, user_categories: list):
    try:
        # Load the model
        tokenizer, model = load_model()
        
        category = categorize_stock(stock_data, blacklist)

        search_prompt = f"""You are StonkSensei, a financial AI assistant.
                  Please give advice on the given stock(s): {', '.join(stock_data)}.

                  Decision Rules:
                  {decision_tree_rules()}

                  User Preferences:
                  - Whitelist: {', '.join(whitelist)}
                  - Blacklist: {', '.join(blacklist)}
                  - Preferred Category: {', '.join(user_categories)}
                  - User's Prompt: {user_prompt}
                  """

        search_inputs = tokenizer(search_prompt, return_tensors="pt").to(model.device)
        prompt_length = search_inputs.input_ids.shape[1]
        
        max_tokens = max(512, getattr(model.config, "max_length", 512))
        
        search_output = model.generate(
            search_inputs.input_ids,
            attention_mask=search_inputs.attention_mask,
            max_new_tokens=max_tokens,
            temperature=0.4,
            do_sample=True
        )
        
        generated_tokens = search_output[0][prompt_length:]
        search_results = tokenizer.decode(generated_tokens, skip_special_tokens=True)

        # Convert the output to JSON format
        response = {
            "ticker": stock_data["ticker"],
            "search_results": search_results.strip()
        }
        
        with open("/tmp/deepseek_results.json", "w") as f:
            json.dump(response, f, indent=4)

        return response
    
    except Exception as e:
        return json.dumps({"error": str(e)})


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
