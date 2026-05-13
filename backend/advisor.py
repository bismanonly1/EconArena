from collections import defaultdict

from db_models import Asset, Holding
from economy import get_latest_indicators
from economy_rules import determine_market_regime


def analyze_portfolio_risk(db):
    holdings = db.query(Holding).all()
    indicators = get_latest_indicators(db)
    market_regime = determine_market_regime(indicators)

    if not holdings:
        return {
            "risk_level": "Low",
            "summary": "You currently hold no assets, so your market risk is low.",
            "warnings": [
                "You are fully in cash and not exposed to market movement."
            ],
            "suggestions": [
                "Start by buying a small quantity of one asset and observe how news affects it."
            ],
            "sector_exposure": {},
            "market_regime": market_regime,
        }

    sector_values = defaultdict(float)
    total_holdings_value = 0
    total_unrealized_pl = 0

    for holding in holdings:
        asset = db.query(Asset).filter(Asset.id == holding.asset_id).first()

        if not asset:
            continue

        current_value = holding.quantity * asset.price
        cost_basis = holding.quantity * holding.average_price
        unrealized_pl = current_value - cost_basis

        sector_values[asset.sector] += current_value
        total_holdings_value += current_value
        total_unrealized_pl += unrealized_pl

    sector_exposure = {}

    for sector, value in sector_values.items():
        sector_exposure[sector] = round((value / total_holdings_value) * 100, 2)

    warnings = []
    suggestions = []

    highest_sector = max(sector_exposure, key=sector_exposure.get)
    highest_exposure = sector_exposure[highest_sector]

    if highest_exposure >= 60:
        warnings.append(
            f"Your portfolio is highly concentrated in {highest_sector} at {highest_exposure}% exposure."
        )
        suggestions.append(
            "Consider diversifying across multiple sectors to reduce concentration risk."
        )

    if market_regime == "Inflationary":
        if sector_exposure.get("Technology", 0) > 30:
            warnings.append(
                "Technology exposure is high during an inflationary regime."
            )
            suggestions.append(
                "Inflation and higher rates can pressure growth-sensitive technology assets."
            )

        if sector_exposure.get("Energy", 0) < 20:
            suggestions.append(
                "Energy assets may provide better resilience during inflationary conditions."
            )

    if market_regime == "Recession":
        warnings.append(
            "The economy is showing recessionary pressure."
        )
        suggestions.append(
            "Defensive sectors such as Healthcare may reduce downside risk."
        )

    if market_regime == "Panic":
        warnings.append(
            "Market fear is elevated, which can increase volatility and sharp price swings."
        )
        suggestions.append(
            "Avoid overtrading and consider holding more cash during panic regimes."
        )

    if indicators.fear_index >= 50:
        warnings.append(
            "Fear Index is elevated, meaning market volatility risk is higher."
        )

    if total_unrealized_pl < 0:
        warnings.append(
            f"Your portfolio currently has an unrealized loss of ${round(total_unrealized_pl, 2)}."
        )
        suggestions.append(
            "Review whether losses are caused by temporary market volatility or poor sector exposure."
        )

    if not warnings:
        warnings.append(
            "No major portfolio risk detected based on current holdings and macro conditions."
        )

    if not suggestions:
        suggestions.append(
            "Continue monitoring market events, macro indicators, and sector exposure."
        )

    if market_regime in ["Panic", "Recession"]:
        risk_level = "High"
    elif highest_exposure >= 60 or indicators.fear_index >= 50:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    summary = (
        f"Your portfolio is currently in a {market_regime} market regime. "
        f"Your largest exposure is {highest_sector} at {highest_exposure}%. "
        f"Total unrealized P/L is ${round(total_unrealized_pl, 2)}."
    )

    return {
        "risk_level": risk_level,
        "summary": summary,
        "warnings": warnings,
        "suggestions": suggestions,
        "sector_exposure": sector_exposure,
        "market_regime": market_regime,
    }