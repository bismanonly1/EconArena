assets = [
    {"id": 1, "name": "TechNova", "sector": "Technology", "price": 100.0, "volatility": 0.08},
    {"id": 2, "name": "EnergyMax", "sector": "Energy", "price": 80.0, "volatility": 0.10},
    {"id": 3, "name": "HealthCore", "sector": "Healthcare", "price": 60.0, "volatility": 0.05},
    {"id": 4, "name": "BankTrust", "sector": "Banking", "price": 90.0, "volatility": 0.07},
    {"id": 5, "name": "DefenseShield", "sector": "Defense", "price": 110.0, "volatility": 0.09}
]

def get_assets():
    return assets

def apply_news_to_market(news_event):
    affected_sector = news_event["sector"]
    sentiment = news_event["sentiment"]
    severity = news_event["severity"]

    for asset in assets:
        if asset["sector"] == affected_sector:
            if sentiment == "positive":
                asset["price"] = round(asset["price"] * (1 + severity), 2)
            else:
                asset["price"] = round(asset["price"] * (1 - severity), 2)

    return assets