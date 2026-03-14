import streamlit as st
import pandas as pd
import requests

BACKEND_URL = "https://socialsent-backend.onrender.com/analyze-batch"
YOUTUBE_URL = "https://socialsent-backend.onrender.com/analyze-youtube"

st.set_page_config(page_title="SocialSent – Comment Analyzer", layout="wide")
st.title("🧠 SocialSent: Sentiment & Toxicity Analyzer")
st.markdown("Upload a CSV of comments to get instant sentiment + toxicity insights.")

st.subheader("🎥 Analyze YouTube Video Comments")
video_url = st.text_input("Paste a YouTube video URL")

if video_url and st.button("🔍 Analyze YouTube Comments"):
    with st.spinner("Fetching and analyzing comments..."):
        res = requests.post(
            YOUTUBE_URL,
            json={"url": video_url, "limit": 50}
        )

    if res.status_code == 200:
        results = res.json()["results"]
        result_df = pd.DataFrame(results)

        st.bar_chart(result_df["sentiment"].value_counts())
        st.bar_chart(result_df.explode("toxicity")["toxicity"].value_counts())
        st.dataframe(result_df)

        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download YouTube Results", data=csv, file_name="youtube_comments.csv")
    else:
        st.error("Failed to fetch/analyze YouTube comments.")


# --- Upload CSV ---
uploaded_file = st.file_uploader("📁 Upload comments CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    if 'comment' not in df.columns:
        st.error("❌ CSV must have a 'comment' column.")
    else:
        with st.spinner("Analyzing comments..."):
            files = {"file": uploaded_file.getvalue()}
            res = requests.post(BACKEND_URL, files=files)

        if res.status_code == 200:
            results = res.json()["results"]
            result_df = pd.DataFrame(results)

            # --- Visualizations ---
            st.subheader("📈 Sentiment Distribution")
            st.bar_chart(result_df["sentiment"].value_counts())

            st.subheader("⚠️ Toxicity Labels")
            exploded = result_df.explode("toxicity")
            st.bar_chart(exploded["toxicity"].value_counts())

            st.subheader("📝 Analyzed Comments")
            st.dataframe(result_df)

            # --- Download button ---
            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download results as CSV", data=csv, file_name="analysis_results.csv", mime="text/csv")

        else:
            st.error("⚠️ Failed to get results from backend.")
