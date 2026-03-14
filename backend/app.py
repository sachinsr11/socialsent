from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
import pandas as pd
import io

from utils.youtube_api import fetch_comments
from analyze import analyze_sentiment, analyze_toxicity

app = FastAPI()

class CommentRequest(BaseModel):
    text: str

class VideoRequest(BaseModel):
    url: str
    limit: int = 50


@app.post("/analyze")
async def analyze_single_comment(payload: CommentRequest):
    sentiment = await analyze_sentiment(payload.text)
    toxicity = await analyze_toxicity(payload.text)
    return {"sentiment": sentiment, "toxicity": toxicity}

@app.post("/analyze-batch")
async def analyze_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    results = []
    for comment in df['comment'].tolist():
        sentiment = await analyze_sentiment(comment)
        toxicity = await analyze_toxicity(comment)
        results.append({
            "comment": comment,
            "sentiment": sentiment,
            "toxicity": toxicity
        })

    return {"results": results}

@app.post("/analyze-youtube")
async def analyze_youtube_video(req: VideoRequest):
    comments = fetch_comments(req.url, req.limit)

    results = []
    for comment in comments:
        sentiment = await analyze_sentiment(comment)
        toxicity = await analyze_toxicity(comment)
        results.append({
            "comment": comment,
            "sentiment": sentiment,
            "toxicity": toxicity
        })

    return {"results": results}
