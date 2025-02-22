import modal
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import json
from pathlib import Path

app = modal.App(name="stonksensei-web-search")

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
SMALL_MODEL = "deepseek-ai/deepseek-llm-7b-chat"

def load_model():
    """Load the small DeepSeek model with 4-bit quantization and trust_remote_code"""
    # Configure 4-bit quantization
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        # bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    tokenizer = AutoTokenizer.from_pretrained(SMALL_MODEL, cache_dir=CACHE_DIR, local_files_only=False)
    model = AutoModelForCausalLM.from_pretrained(
        SMALL_MODEL,
        device_map="auto",
        quantization_config=quantization_config,
        trust_remote_code=True,
        cache_dir=CACHE_DIR,
        local_files_only=False
    )
    return tokenizer, model

@app.function(image=image, gpu="h100", volumes={CACHE_DIR: volume}, timeout=1800)
def generate_recommendation(stock_data: dict, whitelist: list, blacklist: list):
    try:
        # Load the small model
        tokenizer, model = load_model()
        
        # 1. Search with DeepSeek ------------------------------------------
        search_prompt = f"""Search the internet and find 3 precise, recent, and credible news articles 
        about {stock_data['ticker']} stock from financial websites.
        Do not search from these websites: {blacklist}.
        Try to include search queries from these websites {whitelist}.
        Focus on these topics:
        - Market trends
        - Earnings reports
        - Analyst opinions
        - Regulatory changes
        Timeframe: Last 7 days.
        Please return the news article titles and the links to the articles in JSON format.
        Do NOT give me code to do this, directly search the web."""

        search_inputs = tokenizer(search_prompt, return_tensors="pt").to(model.device)
        prompt_length = search_inputs.input_ids.shape[1]
        
        max_tokens = min(300, getattr(model.config, "max_length", 512))
        
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

# Example usage for local testing (will run on Modal when deployed)
# if __name__ == "__main__":
#     stock_data_example = {
#         "ticker": "AAPL",
#         "risk": 25,
#         "sentiment": 8.2,
#         "hype": 6.5
#     }
    
#     result = generate_recommendation.remote(
#         stock_data=stock_data_example,
#         whitelist=["bloomberg.com", "reuters.com"],
#         blacklist=["example.com"]
#     )
    
#     print(result)