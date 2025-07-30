from dotenv import load_dotenv
load_dotenv()

import httpx
import os

HF_API_KEY = os.getenv("HF_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# Sentiment Model: CardiffNLP
SENTIMENT_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
# Toxicity Model: Unitary
TOXICITY_URL = "https://api-inference.huggingface.co/models/unitary/toxic-bert"

LABEL_MAP = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
}

async def analyze_sentiment(comment: str) -> str:
    async with httpx.AsyncClient() as client:
        res = await client.post(SENTIMENT_URL, headers=HEADERS, json={"inputs": comment})
        if res.status_code == 200:
            scores = res.json()[0]
            label = max(scores, key=lambda x: x["score"])["label"]
            return LABEL_MAP.get(label, label)
        return "Unknown"

async def analyze_toxicity(comment: str) -> list:
    async with httpx.AsyncClient() as client:
        res = await client.post(TOXICITY_URL, headers=HEADERS, json={"inputs": comment})
        if res.status_code == 200:
            labels = [x["label"] for x in res.json()[0] if x["score"] > 0.5]
            return labels or ["Non-toxic"]
        return ["Unknown"]
