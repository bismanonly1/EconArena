from fastapi import FastAPI
from market import get_assets, apply_news_to_market
from news import generate_news
from pydantic import BaseModel
from trading import get_portfolio, buy_asset, sell_asset
from explanation import explain_market_event

class TradeRequest(BaseModel):
    asset_id: int
    quantity: int

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

@app.get("/portfolio")
def portfolio():
    return get_portfolio()

@app.post ("/trade/buy")
def buy(request: TradeRequest):
    return buy_asset(request.asset_id, request.quantity, get_assets())

@app.post("/trade/sell")
def sell(request: TradeRequest):
    return sell_asset(request.asset_id, request.quantity, get_assets())

@app.get("/market/stimulate-event")
def simulate_market_event():
    news_event = generate_news()
    updated_assets = apply_news_to_market(news_event)
    explanation = explain_market_event(news_event)

    return {
        "news": news_event,
        "updated_assets": updated_assets,
        "ai_explanation": explanation
    }