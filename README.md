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
