from economy_rules import determine_market_regime


def explain_market_event(news_event, indicators=None):
    sector = news_event["sector"]
    sentiment = news_event["sentiment"]
    severity = news_event["severity"]
    title = news_event["title"]

    direction = "increased" if sentiment == "positive" else "decreased"

    base_explanation = (
        f"The {sector} sector initially {direction} because this news created "
        f"{sentiment} sentiment. The event severity was {round(severity * 100, 2)}%."
    )

    if not indicators:
        return {
            "headline": title,
            "explanation": base_explanation,
            "learning_point": (
                f"This shows how {sector} assets react to news sentiment "
                f"and perceived economic impact."
            ),
        }

    regime = determine_market_regime(indicators)

    macro_notes = []

    if indicators.inflation >= 5:
        macro_notes.append("elevated inflation is adding pressure to growth-sensitive assets")

    if indicators.interest_rate >= 5:
        macro_notes.append("higher interest rates are affecting valuation-sensitive sectors")

    if indicators.gdp_growth >= 3:
        macro_notes.append("strong GDP growth is supporting risk appetite")

    if indicators.gdp_growth < 0:
        macro_notes.append("negative GDP growth is creating recession pressure")

    if indicators.unemployment >= 8:
        macro_notes.append("high unemployment is weakening the economic outlook")

    if indicators.fear_index >= 50:
        macro_notes.append("high market fear is increasing volatility")

    if not macro_notes:
        macro_notes.append("macro conditions are currently balanced")

    macro_explanation = (
        f"The current market regime is {regime}. "
        f"Macro context: {', '.join(macro_notes)}."
    )

    return {
        "headline": title,
        "explanation": f"{base_explanation} {macro_explanation}",
        "learning_point": (
            "This demonstrates that markets do not move from news alone. "
            "Prices are also shaped by inflation, interest rates, growth, unemployment, "
            "and fear conditions."
        ),
    }