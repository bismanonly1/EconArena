portfolio = {
    "cash": 10000.0,
    "holdings": {}
}

def get_portfolio():
    return portfolio

def buy_asset(asset_id, quantity, assets):
    asset = next((a for a in assets if a["id"] == asset_id), None)

    if not asset:
        return {"error": "Asset not found"}
    total_cost = asset["price"] * quantity

    if portfolio["cash"] < total_cost:
        return {"error": "Not enough cash"}
    portfolio["cash"] = round(portfolio["cash"] - total_cost, 2)
    asset_name = asset["name"]

    if asset_name not in portfolio["holdings"]:
        portfolio["holdings"][asset_name] = {
            "quantity": 0,
            "average_price": asset["price"]
        }
    portfolio["holdings"][asset_name]["quantity"] += quantity

    return {
        "message": "Buy order successful",
        "portfolio": portfolio
    }

def sell_asset(asset_id, quantity, assets):
    asset = next((a for a in assets if a["id"] == asset_id), None)

    if not asset:
        return {"error": "Asset not found"}

    asset_name = asset["name"]

    if asset_name not in portfolio["holdings"]:
        return {"error": "You do not own this asset"}

    if portfolio["holdings"][asset_name]["quantity"] < quantity:
        return {"error": "Not enough quantity to sell"}

    sale_value = asset["price"] * quantity
    portfolio["cash"] = round(portfolio["cash"] + sale_value, 2)

    portfolio["holdings"][asset_name]["quantity"] -= quantity

    if portfolio["holdings"][asset_name]["quantity"] == 0:
        del portfolio["holdings"][asset_name]

    return {
        "message": "Sell order successful",
        "portfolio": portfolio
    }