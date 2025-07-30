import requests
import os

from dotenv import load_dotenv
load_dotenv()


YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def extract_video_id(url: str) -> str:
    # Basic parsing for watch?v= and short URLs
    if "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    else:
        return url  # Assume it's already a video ID

def fetch_comments(video_url: str, max_comments: int = 50) -> list:
    if not YOUTUBE_API_KEY:
        raise EnvironmentError("Missing YOUTUBE_API_KEY")

    video_id = extract_video_id(video_url)
    comments = []

    base_url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": YOUTUBE_API_KEY,
        "maxResults": 100,
        "textFormat": "plainText"
    }

    while len(comments) < max_comments and params.get("pageToken", True):
        res = requests.get(base_url, params=params)
        if res.status_code != 200:
            break

        data = res.json()
        for item in data.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        params["pageToken"] = data.get("nextPageToken", None)
        if not params["pageToken"]:
            break

    return comments[:max_comments]
