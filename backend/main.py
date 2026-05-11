from fastapi import FastAPI
from market import get_assets
from news import generate_news

app = FastAPI(title="EconArena AI")

@app.get("/")
def home():
    return {
        "message": "EconArena AI backend is running"
    }

@app.get("/market/assets")
def market_assets():
    return get_assets()

@app.get("/news/generate")
def generate_market_news():
    return generate_news()
