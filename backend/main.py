from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from market import get_assets, apply_news_to_market
from news import generate_news
from trading import get_portfolio, buy_asset, sell_asset, get_transactions
from explanation import explain_market_event
from db_models import MarketHistory, Asset, Portfolio, Holding, Transaction, NewsEvent


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

    saved_news = NewsEvent(
        title = news_event["title"],
        sector = news_event["sector"],
        sentiment = news_event["sentiment"],
        severity = news_event["severity"],
    )

    db.add(saved_news)
    db.commit()

    updated_assets = apply_news_to_market(news_event, db)
    explanation = explain_market_event(news_event)

    return {
        "news": news_event,
        "updated_assets": updated_assets,
        "ai_explanation": explanation
    }

@app.get("/news/history")
def news_history(db: Session = Depends(get_db)):
    events = db.query(NewsEvent).order_by(NewsEvent.timestamp.desc()).all()

    return [
        {
            "id": event.id,
            "title": event.title,
            "sector": event.sector,
            "sentiment": event.sentiment,
            "severity": event.severity,
            "timestamp": event.timestamp
        }
        for event in events
    ]


@app.get("/portfolio")
def portfolio(db: Session = Depends(get_db)):
    return get_portfolio(db)

@app.get("/market/history")
def market_history(db: Session = Depends(get_db)):
    history = db.query(MarketHistory).all()

    return [
        {
            "asset_id": item.asset_id,
            "asset_name": item.asset_name,
            "price": item.price,
            "timestamp": item.timestamp
        }
        for item in history
    ]

@app.post("/trade/buy")
def buy(request: TradeRequest, db: Session = Depends(get_db)):
    return buy_asset(
        request.asset_id,
        request.quantity,
        db
    )

@app.get("/transactions")
def transactions(db: Session = Depends(get_db)):
    return get_transactions(db)

@app.post("/trade/sell")
def sell(request: TradeRequest, db: Session = Depends(get_db)):
    return sell_asset(
        request.asset_id,
        request.quantity,
        db
    )

@app.post("/simulation/reset")
def reset_simulation(db: Session = Depends(get_db)):
    db.query(Holding).delete()
    db.query(Transaction).delete()
    db.query(MarketHistory).delete()
    db.query(NewsEvent).delete()

    portfolio = db.query(Portfolio).first()
    if portfolio:
        portfolio.cash = 10000.0

    starter_prices = {
        "TechNova": 100.0,
        "EnergyMax": 80.0,
        "Healthcore": 60.0,
        "BankTrust": 90.0,
        "DefenseShield": 110.0
    }

    assets = db.query(Asset).all()
    for asset in assets:
        if asset.name in starter_prices:
            asset.price = starter_prices[asset.name]

    db.commit()

    return {"message": "Simulation reset successfully"}