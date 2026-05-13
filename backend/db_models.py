from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    sector = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    volatility = Column(Float, nullable=False)


class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True, index=True)
    cash = Column(Float, default=10000.0)


class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, nullable=False)
    asset_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    average_price = Column(Float, nullable=False)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, nullable=False)
    asset_name = Column(String, nullable=False)
    trade_type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    total_value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class NewsEvent(Base):
    __tablename__ = "news_events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    sentiment = Column(String, nullable=False)
    severity = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class MarketHistory(Base):
    __tablename__ = "market_history"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, nullable=False)
    asset_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class EconomicIndicator(Base):
    __tablename__ = "economic_indicators"

    id = Column(Integer, primary_key=True, index=True)
    inflation = Column(Float, default=2.5)
    interest_rate = Column(Float, default=4.5)
    gdp_growth = Column(Float, default=2.0)
    unemployment = Column(Float, default=5.5)
    fear_index = Column(Float, default=20.0)
    timestamp = Column(DateTime, default=datetime.utcnow)