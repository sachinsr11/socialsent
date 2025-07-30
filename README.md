# SocialSent

## Overview
SocialSent is a Python toolkit and web app for analyzing sentiment and toxicity in social media comments. It supports batch analysis via CSV upload and direct YouTube video comment analysis.

## Features
- Sentiment & toxicity analysis using HuggingFace models
- Analyze YouTube video comments directly
- Upload CSVs for batch analysis
- Interactive Streamlit frontend
- FastAPI backend

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Clone the Repository
```bash
git clone https://github.com/yourusername/socialsent.git
cd socialsent
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the `backend/` directory with the following contents:

```
HF_API_KEY=your_huggingface_api_key
YOUTUBE_API_KEY=your_youtube_api_key
```

- `HF_API_KEY`: Get your API key from [HuggingFace](https://huggingface.co/settings/tokens).
- `YOUTUBE_API_KEY`: Get your API key from [Google Cloud Console](https://console.cloud.google.com/apis/credentials).

### Running the Backend

Start the FastAPI backend (from the project root):

```bash
cd backend
uvicorn app:app --reload
```

### Running the Frontend

Start the Streamlit frontend (from the project root):

```bash
cd frontend
streamlit run streamlit_app.py
```

### Usage

1. Open the Streamlit app in your browser (usually at `http://localhost:8501`).
2. Paste a YouTube video URL or upload a CSV file containing a `comment` column.
3. View sentiment and toxicity analysis results, download CSVs.

### Example CSV Format

```
comment
This is awesome!
I hate this.
Neutral statement here.
```

### Troubleshooting

- **Missing API Keys**: Ensure your `.env` file is present and contains valid keys.
- **Backend Not Running**: Make sure the FastAPI server is running before using the frontend.
- **CSV Errors**: Uploaded CSV must have a `comment` column.

## Project Structure
```
socialsent/
├── backend/
│   ├── app.py
│   ├── analyze.py
│   ├── utils/
│   │   └── youtube_api.py
│   └── .env
├── frontend/
│   └── streamlit_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## License
MIT