import os
from huggingface_hub import InferenceClient

# Load Hugging Face API key
HF_API_KEY = os.getenv("HF_API_KEY") or os.getenv("HF_TOKEN")
if HF_API_KEY is None:
    raise EnvironmentError("HF_API_KEY or HF_TOKEN environment variable is required.")

# Create Hugging Face client
client = InferenceClient(
    provider="hf-inference",
    api_key=HF_API_KEY,
)

# Models
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
TOXICITY_MODEL = "unitary/unbiased-toxic-roberta"

# Sentiment label mapping
LABEL_MAP = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
}

# --- Functions ---
async def analyze_sentiment(comment: str) -> str:
    try:
        results = client.text_classification(comment, model=SENTIMENT_MODEL)
        # results is a list of dicts: [{"label": "LABEL_2", "score": 0.98}, ...]
        label = max(results, key=lambda x: x["score"])["label"]
        return LABEL_MAP.get(label, label)
    except Exception as e:
        print("Sentiment API error:", e)
        return "Unknown"

async def analyze_toxicity(comment: str) -> list:
    try:
        results = client.text_classification(comment, model=TOXICITY_MODEL)
        labels = [x["label"] for x in results if x["score"] > 0.5]
        return labels or ["Non-toxic"]
    except Exception as e:
        print("Toxicity API error:", e)
        return ["Unknown"]
