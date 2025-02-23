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
MODEL_NAME = "deepseek-ai/deepseek-llm-7b-chat"

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
def generate_recommendation(user_prompt: str, stock_data: list[dict], amount: str, user_risk: str):
    try:
        # Load the model
        tokenizer, model = load_model()
                
        # Format the stats for each remaining stock:
        # Each stock is represented as "Name (Hype: X, Risk: Y, Sentiment: Z)"
        formatted_stats = [
            f'{stock["ticker"]} (Hype: {stock["hype"]}, Risk: {stock["risk"]}, Sentiment: {stock["sentiment_score"]})'
            for stock in stock_data
        ]
        
        stocks_info = ", ".join(formatted_stats)
                 
        search_prompt = f"""You are StonkSensei, a financial AI assistant. Your task is to help the user make money.
                  Please give advice on the given stock(s): {stocks_info}.

                  Decision Rules:
                  {decision_tree_rules()}

                  User Preferences:
                  - Investment Amount: {amount}
                  - Preferred Categories: {user_risk}
                  - User's Prompt: {user_prompt}
                  
                  Please get the top 3 stocks to invest in and categorize them based on the given stats and decision rules.

                  Can you give me a list of JSON objects with only these entries per object so I can directly send this to my API:
                  - Ticker
                  - Category (⚠️ YOLO Pick, ✅ Consider Buying, ✅ Strong Buy)
                  - Reason (This is general advice on why this stock might be worth investing)
                  """

        search_inputs = tokenizer(search_prompt, return_tensors="pt").to(model.device)
        prompt_length = search_inputs.input_ids.shape[1]
        
        max_tokens = 512
                
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
            "recommendations": search_results.strip()
        }
        
        with open("/tmp/deepseek_results.json", "w") as f:
            json.dump(response, f, indent=4)

        return response
    
    except Exception as e:
        return json.dumps({"error": str(e)})


def decision_tree_rules() -> str:
    return """
            Hype varies.
            Risk varies.
            Sentiment is a value from -1 to 1
            Low Risk + High Sentiment + High Hype → ✅ Strong Buy
            Low Risk + Low Sentiment + High Hype → ❌ Avoid
            Medium Risk + High Sentiment + Medium Hype → ✅ Consider Buying
            High Risk + High Sentiment + High Hype → ⚠️ YOLO Pick
            High Risk + Low Sentiment + Low Hype → ❌ Avoid
            """


def clean_response(text: str) -> str:
    """Clean up LLM output by removing system tokens if any."""
    # This example assumes a token like '[/INST]' might be in the output.
    return text.split("[/INST]")[-1].strip()
