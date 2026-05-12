from db_models import Asset, Portfolio, Holding, Transaction


def get_portfolio(db):
    portfolio = db.query(Portfolio).first()
    holdings = db.query(Holding).all()

    return {
        "cash": portfolio.cash,
        "holdings": [
            {
                "asset_id": holding.asset_id,
                "asset_name": holding.asset_name,
                "quantity": holding.quantity,
                "average_price": holding.average_price
            }
            for holding in holdings
        ]
    }


def buy_asset(asset_id, quantity, db):
    if quantity <= 0:
        return {"error": "Quantity must be greater than zero"}

    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:
        return {"error": "Asset not found"}

    portfolio = db.query(Portfolio).first()
    total_cost = round(asset.price * quantity, 2)

    if portfolio.cash < total_cost:
        return {"error": "Not enough cash"}

    portfolio.cash = round(portfolio.cash - total_cost, 2)

    holding = db.query(Holding).filter(
        Holding.asset_id == asset_id
    ).first()

    if holding:
        old_total = holding.quantity * holding.average_price
        new_total = quantity * asset.price
        new_quantity = holding.quantity + quantity

        holding.quantity = new_quantity
        holding.average_price = round((old_total + new_total) / new_quantity, 2)
    else:
        holding = Holding(
            asset_id=asset.id,
            asset_name=asset.name,
            quantity=quantity,
            average_price=asset.price
        )
        db.add(holding)

    transaction = Transaction(
        asset_id=asset.id,
        asset_name=asset.name,
        trade_type="BUY",
        quantity=quantity,
        price=asset.price,
        total_value=total_cost
    )

    db.add(transaction)
    db.commit()

    return {
        "message": "Buy order successful",
        "portfolio": get_portfolio(db)
    }


def sell_asset(asset_id, quantity, db):
    if quantity <= 0:
        return {"error": "Quantity must be greater than zero"}

    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:
        return {"error": "Asset not found"}

    holding = db.query(Holding).filter(
        Holding.asset_id == asset_id
    ).first()

    if not holding:
        return {"error": "You do not own this asset"}

    if holding.quantity < quantity:
        return {"error": "Not enough quantity to sell"}

    portfolio = db.query(Portfolio).first()
    sale_value = round(asset.price * quantity, 2)

    portfolio.cash = round(portfolio.cash + sale_value, 2)
    holding.quantity -= quantity

    if holding.quantity == 0:
        db.delete(holding)

    transaction = Transaction(
        asset_id=asset.id,
        asset_name=asset.name,
        trade_type="SELL",
        quantity=quantity,
        price=asset.price,
        total_value=sale_value
    )

    db.add(transaction)
    db.commit()

    return {
        "message": "Sell order successful",
        "portfolio": get_portfolio(db)
    }


def get_transactions(db):
    transactions = db.query(Transaction).order_by(
        Transaction.timestamp.desc()
    ).all()

    return [
        {
            "id": transaction.id,
            "asset_name": transaction.asset_name,
            "trade_type": transaction.trade_type,
            "quantity": transaction.quantity,
            "price": transaction.price,
            "total_value": transaction.total_value,
            "timestamp": transaction.timestamp
        }
        for transaction in transactions
    ]