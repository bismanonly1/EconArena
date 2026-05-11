from fastapi import FastAPI
from market import get_assets, apply_news_to_market
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

@app.get("/market/simulate-event")
def simulate_market_event():
    news_event = generate_news()
    updated_assets = apply_news_to_market(news_event)

    return {
        "news": news_event,
        "updated_assets": updated_assets
    }
