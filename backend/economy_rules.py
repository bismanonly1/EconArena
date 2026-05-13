def determine_market_regime(indicators):
    inflation = indicators.inflation
    interest_rate = indicators.interest_rate
    gdp_growth = indicators.gdp_growth
    unemployment = indicators.unemployment
    fear_index = indicators.fear_index

    if fear_index >= 70:
        return "Panic"

    if gdp_growth < 0 or unemployment >= 8:
        return "Recession"

    if inflation >= 5 and interest_rate >= 5:
        return "Inflationary"

    if gdp_growth >= 3 and unemployment <= 5:
        return "Expansion"

    return "Neutral"


SECTOR_MACRO_SENSITIVITY = {
    "Technology": {
        "inflation": -0.004,
        "interest_rate": -0.005,
        "gdp_growth": 0.006,
        "unemployment": -0.003,
        "fear_index": -0.002,
    },
    "Energy": {
        "inflation": 0.005,
        "interest_rate": -0.001,
        "gdp_growth": 0.003,
        "unemployment": -0.001,
        "fear_index": 0.002,
    },
    "Healthcare": {
        "inflation": -0.001,
        "interest_rate": -0.001,
        "gdp_growth": 0.001,
        "unemployment": 0.000,
        "fear_index": 0.001,
    },
    "Banking": {
        "inflation": -0.002,
        "interest_rate": 0.003,
        "gdp_growth": 0.004,
        "unemployment": -0.004,
        "fear_index": -0.003,
    },
    "Defense": {
        "inflation": 0.001,
        "interest_rate": -0.001,
        "gdp_growth": 0.001,
        "unemployment": 0.000,
        "fear_index": 0.004,
    },
}


REGIME_ADJUSTMENTS = {
    "Expansion": {
        "Technology": 0.015,
        "Energy": 0.008,
        "Healthcare": 0.004,
        "Banking": 0.012,
        "Defense": 0.002,
    },
    "Inflationary": {
        "Technology": -0.018,
        "Energy": 0.018,
        "Healthcare": -0.003,
        "Banking": 0.004,
        "Defense": 0.008,
    },
    "Recession": {
        "Technology": -0.020,
        "Energy": -0.012,
        "Healthcare": 0.006,
        "Banking": -0.018,
        "Defense": 0.004,
    },
    "Panic": {
        "Technology": -0.035,
        "Energy": -0.010,
        "Healthcare": -0.004,
        "Banking": -0.030,
        "Defense": 0.018,
    },
    "Neutral": {
        "Technology": 0.000,
        "Energy": 0.000,
        "Healthcare": 0.000,
        "Banking": 0.000,
        "Defense": 0.000,
    },
}


def calculate_macro_pressure(asset_sector, indicators):
    sensitivity = SECTOR_MACRO_SENSITIVITY.get(asset_sector, {})

    pressure = 0

    pressure += indicators.inflation * sensitivity.get("inflation", 0)
    pressure += indicators.interest_rate * sensitivity.get("interest_rate", 0)
    pressure += indicators.gdp_growth * sensitivity.get("gdp_growth", 0)
    pressure += indicators.unemployment * sensitivity.get("unemployment", 0)
    pressure += indicators.fear_index * sensitivity.get("fear_index", 0)

    regime = determine_market_regime(indicators)

    pressure += REGIME_ADJUSTMENTS.get(regime, {}).get(asset_sector, 0)

    return round(pressure, 4)


def explain_macro_pressure(asset_sector, indicators):
    regime = determine_market_regime(indicators)

    explanations = []

    if indicators.inflation >= 5:
        explanations.append("inflation is elevated")

    if indicators.interest_rate >= 5:
        explanations.append("interest rates are restrictive")

    if indicators.gdp_growth >= 3:
        explanations.append("GDP growth is strong")

    if indicators.gdp_growth < 0:
        explanations.append("GDP growth is negative")

    if indicators.unemployment >= 8:
        explanations.append("unemployment is high")

    if indicators.fear_index >= 50:
        explanations.append("market fear is elevated")

    if not explanations:
        explanations.append("macro conditions are relatively balanced")

    return {
        "sector": asset_sector,
        "market_regime": regime,
        "macro_summary": ", ".join(explanations),
    }