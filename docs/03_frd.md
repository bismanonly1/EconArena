# Functional Requirements Document — MarketPulse AI

## Feature 1: Market Dashboard
The user must see available assets, prices, sectors, and daily percentage change.

## Feature 2: Trading
The user must be able to buy and sell simulated assets.

## Feature 3: Portfolio
The user must see:
- cash balance
- owned assets
- quantity
- average price
- total portfolio value
- profit/loss

## Feature 4: AI News Engine
The system must generate simulated financial news.

Each news event must include:
- title
- category
- affected sector
- sentiment
- severity

## Feature 5: Market Reaction Engine
The system must update prices based on:
- sector
- sentiment
- severity
- volatility

## Feature 6: AI Explanation Engine
The system must explain:
- why prices moved
- which sector was affected
- how the user’s portfolio changed

## User Story Example
As a beginner trader, I want to understand why my asset price changed so I can learn market logic.

## Acceptance Criteria
- Given a news event is generated, affected assets should change price.
- Given a user buys an asset, portfolio quantity should increase.
- Given a user sells an asset, cash balance should increase.
- Given prices change, portfolio value should update.