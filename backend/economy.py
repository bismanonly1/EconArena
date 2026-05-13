from db_models import EconomicIndicator


def get_latest_indicators(db):
    indicators = db.query(EconomicIndicator).order_by(
        EconomicIndicator.timestamp.desc()
    ).first()

    if not indicators:
        indicators = EconomicIndicator(
            inflation=2.5,
            interest_rate=4.5,
            gdp_growth=2.0,
            unemployment=5.5,
            fear_index=20.0
        )
        db.add(indicators)
        db.commit()
        db.refresh(indicators)

    return indicators


def serialize_indicators(indicators):
    return {
        "inflation": indicators.inflation,
        "interest_rate": indicators.interest_rate,
        "gdp_growth": indicators.gdp_growth,
        "unemployment": indicators.unemployment,
        "fear_index": indicators.fear_index,
        "timestamp": indicators.timestamp,
    }


def update_economic_indicators(news_event, db):
    current = get_latest_indicators(db)

    inflation = current.inflation
    interest_rate = current.interest_rate
    gdp_growth = current.gdp_growth
    unemployment = current.unemployment
    fear_index = current.fear_index

    sector = news_event["sector"]
    sentiment = news_event["sentiment"]
    severity = news_event["severity"]

    direction = 1 if sentiment == "positive" else -1

    if sector == "Energy":
        inflation += severity * 2.0 * direction
        fear_index += severity * 10.0

    elif sector == "Banking":
        interest_rate += severity * 0.5 * direction
        fear_index += severity * 8.0 if sentiment == "negative" else -severity * 4.0

    elif sector == "Technology":
        gdp_growth += severity * 1.5 * direction
        fear_index += -severity * 5.0 if sentiment == "positive" else severity * 8.0

    elif sector == "Healthcare":
        unemployment += -severity * 0.3 if sentiment == "positive" else severity * 0.3
        fear_index += -severity * 3.0 if sentiment == "positive" else severity * 5.0

    elif sector == "Defense":
        fear_index += severity * 12.0
        inflation += severity * 0.5

    inflation = round(max(0.0, min(inflation, 15.0)), 2)
    interest_rate = round(max(0.0, min(interest_rate, 12.0)), 2)
    gdp_growth = round(max(-8.0, min(gdp_growth, 8.0)), 2)
    unemployment = round(max(2.0, min(unemployment, 20.0)), 2)
    fear_index = round(max(0.0, min(fear_index, 100.0)), 2)

    updated = EconomicIndicator(
        inflation=inflation,
        interest_rate=interest_rate,
        gdp_growth=gdp_growth,
        unemployment=unemployment,
        fear_index=fear_index,
    )

    db.add(updated)
    db.commit()
    db.refresh(updated)

    return serialize_indicators(updated)