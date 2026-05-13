import random

from db_models import Asset, MarketHistory


SECTOR_CORRELATIONS = {
    "Technology": {
        "Banking": 0.02,
        "Healthcare": 0.01,
        "Energy": -0.01,
        "Defense": 0.01,
    },
    "Energy": {
        "Technology": -0.02,
        "Banking": -0.01,
        "Healthcare": 0.00,
        "Defense": 0.03,
    },
    "Healthcare": {
        "Technology": 0.01,
        "Banking": 0.00,
        "Energy": 0.00,
        "Defense": 0.00,
    },
    "Banking": {
        "Technology": 0.02,
        "Energy": 0.01,
        "Healthcare": 0.00,
        "Defense": -0.01,
    },
    "Defense": {
        "Energy": 0.02,
        "Technology": 0.01,
        "Banking": -0.01,
        "Healthcare": 0.00,
    },
}


def get_assets(db):
    assets = db.query(Asset).all()

    return [
        {
            "id": asset.id,
            "name": asset.name,
            "sector": asset.sector,
            "price": asset.price,
            "volatility": asset.volatility,
        }
        for asset in assets
    ]


def calculate_price_change(asset, base_impact):
    market_noise = random.uniform(-0.015, 0.015)

    volatility_multiplier = random.uniform(0.5, 1.5)

    volatility_adjustment = abs(base_impact) * asset.volatility * volatility_multiplier

    if base_impact >= 0:
        final_impact = base_impact + volatility_adjustment + market_noise
    else:
        final_impact = base_impact - volatility_adjustment + market_noise

    return final_impact


def apply_price_change(asset, impact):
    old_price = asset.price
    new_price = round(old_price * (1 + impact), 2)

    if new_price < 1:
        new_price = 1

    asset.price = new_price

    return {
        "asset_name": asset.name,
        "sector": asset.sector,
        "old_price": old_price,
        "new_price": new_price,
        "impact_percent": round(impact * 100, 2),
    }


def save_market_history(asset, db):
    history = MarketHistory(
        asset_id=asset.id,
        asset_name=asset.name,
        price=asset.price,
    )

    db.add(history)


def apply_news_to_market(news_event, db):
    affected_sector = news_event["sector"]
    sentiment = news_event["sentiment"]
    severity = news_event["severity"]

    if sentiment == "positive":
        main_impact = severity
    else:
        main_impact = -severity

    market_movements = []

    all_assets = db.query(Asset).all()

    for asset in all_assets:
        if asset.sector == affected_sector:
            impact = calculate_price_change(asset, main_impact)
        else:
            sector_correlation = SECTOR_CORRELATIONS.get(
                affected_sector, {}
            ).get(asset.sector, 0)

            impact = calculate_price_change(asset, sector_correlation)

        movement = apply_price_change(asset, impact)
        market_movements.append(movement)

        save_market_history(asset, db)

    db.commit()

    return {
        "updated_assets": get_assets(db),
        "market_movements": market_movements,
    }