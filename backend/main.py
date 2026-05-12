from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from market import get_assets, apply_news_to_market
from news import generate_news
from trading import get_portfolio, buy_asset, sell_asset, get_transactions
from explanation import explain_market_event


app = FastAPI(title="EconArena AI")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TradeRequest(BaseModel):
    asset_id: int
    quantity: int


@app.get("/")
def home():
    return {
        "message": "EconArena AI backend is running"
    }


@app.get("/market/assets")
def market_assets(db: Session = Depends(get_db)):
    return get_assets(db)


@app.get("/news/generate")
def generate_market_news():
    return generate_news()


@app.get("/market/simulate-event")
def simulate_market_event(db: Session = Depends(get_db)):
    news_event = generate_news()
    updated_assets = apply_news_to_market(news_event, db)
    explanation = explain_market_event(news_event)

    return {
        "news": news_event,
        "updated_assets": updated_assets,
        "ai_explanation": explanation
    }


@app.get("/portfolio")
def portfolio(db: Session = Depends(get_db)):
    return get_portfolio(db)


@app.get("/transactions")
def transactions(db: Session = Depends(get_db)):
    return get_transactions(db)


@app.post("/trade/buy")
def buy(request: TradeRequest, db: Session = Depends(get_db)):
    return buy_asset(
        request.asset_id,
        request.quantity,
        db
    )


@app.post("/trade/sell")
def sell(request: TradeRequest, db: Session = Depends(get_db)):
    return sell_asset(
        request.asset_id,
        request.quantity,
        db
    )