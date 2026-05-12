from db_models import Asset


def get_assets(db):
    assets = db.query(Asset).all()

    return [
        {
            "id": asset.id,
            "name": asset.name,
            "sector": asset.sector,
            "price": asset.price,
            "volatility": asset.volatility
        }
        for asset in assets
    ]


def apply_news_to_market(news_event, db):
    affected_sector = news_event["sector"]
    sentiment = news_event["sentiment"]
    severity = news_event["severity"]

    affected_assets = db.query(Asset).filter(
        Asset.sector == affected_sector
    ).all()

    for asset in affected_assets:
        if sentiment == "positive":
            asset.price = round(asset.price * (1 + severity), 2)
        else:
            asset.price = round(asset.price * (1 - severity), 2)

    db.commit()

    return get_assets(db)