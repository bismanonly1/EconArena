# EconArena AI

EconArena AI is a full-stack AI-powered financial simulation and Canadian market paper-trading platform. It combines real Canadian market data with virtual trading, portfolio analytics, and an AI-driven macroeconomic training simulator.

## What It Does

EconArena AI has two modes:

### 1. Real Canadian Market Mode
Users can explore Canadian stocks, ETFs, bond ETFs, gold ETFs, and cash ETFs by sector, asset class, and risk level. They can virtually buy and sell real Canadian assets using live market prices and track portfolio performance over time.

### 2. AI Economic Training Simulator
Users can trigger simulated economic events such as inflation shocks, banking pressure, energy disruptions, and technology booms. The system updates macroeconomic indicators, determines market regimes, moves simulated assets, and explains why prices changed.

## Key Features

- Real Canadian market asset universe
- Virtual paper trading with real market prices
- Canadian stocks, ETFs, bond ETFs, gold ETFs, and cash ETFs
- Sector and asset-class filtering
- Portfolio cash, holdings, total value, and unrealized P/L
- Real-market transaction history
- AI-generated economic simulation mode
- Macroeconomic indicators: inflation, rates, GDP growth, unemployment, fear index
- Market regime detection: Neutral, Expansion, Inflationary, Recession, Panic
- Market movement breakdown with macro pressure
- AI portfolio advisor for risk, warnings, and suggestions

## Tech Stack

### Frontend
- Next.js
- React
- JavaScript
- Tailwind CSS
- Axios
- Recharts

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- yfinance

## Project Architecture

```text
Frontend: Next.js + React + Tailwind
        ↓
API Layer: Axios
        ↓
Backend: FastAPI
        ↓
Database: SQLite + SQLAlchemy
        ↓
Market Data: yfinance

### Current Status

This project is currently a working MVP. It supports real Canadian market paper trading and AI-powered simulated economic training.

How To Run Locally
Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

Backend runs at:

http://127.0.0.1:8000
Frontend
cd frontend
npm install
npm run dev

Frontend runs at:

http://localhost:3000
API Examples
Real Canadian Market
GET /real-market/categories
GET /real-market/universe
GET /real-market/quote/RY.TO
GET /real-market/quotes?sector=Banking
GET /real-portfolio
POST /real-trade/buy
POST /real-trade/sell
AI Simulation
GET /market/assets
GET /market/simulate-event
GET /portfolio
GET /economy/indicators
GET /advisor/portfolio
Roadmap
Add user authentication
Add PostgreSQL support
Add real-market charts per asset
Add benchmark comparison against XIU.TO or XIC.TO
Add AI-generated financial explanations
Add episode-based learning scenarios
Add deployment with Docker
Add CI/CD pipeline
Disclaimer

This application is for educational and simulation purposes only. It does not provide financial advice or execute real trades.