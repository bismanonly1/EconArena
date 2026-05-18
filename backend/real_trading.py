from db_models import RealPortfolio, RealHolding, RealTransaction
from real_market import get_quote


def get_or_create_real_portfolio(db):
    portfolio = db.query(RealPortfolio).first()

    if not portfolio:
        portfolio = RealPortfolio(cash=10000.0)
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)

    return portfolio


def get_real_portfolio(db):
    portfolio = get_or_create_real_portfolio(db)
    holdings = db.query(RealHolding).all()

    holdings_data = []
    holdings_value = 0
    total_unrealized_pl = 0

    for holding in holdings:
        quote = get_quote(holding.symbol)

        if "error" in quote:
            current_price = holding.average_price
        else:
            current_price = quote["price"]

        current_value = round(holding.quantity * current_price, 2)
        cost_basis = round(holding.quantity * holding.average_price, 2)
        unrealized_pl = round(current_value - cost_basis, 2)

        holdings_value += current_value
        total_unrealized_pl += unrealized_pl

        holdings_data.append({
            "symbol": holding.symbol,
            "name": holding.name,
            "asset_class": holding.asset_class,
            "sector": holding.sector,
            "quantity": holding.quantity,
            "average_price": holding.average_price,
            "current_price": current_price,
            "current_value": current_value,
            "unrealized_pl": unrealized_pl,
        })

    total_portfolio_value = round(portfolio.cash + holdings_value, 2)

    return {
        "cash": round(portfolio.cash, 2),
        "holdings_value": round(holdings_value, 2),
        "total_portfolio_value": total_portfolio_value,
        "total_unrealized_pl": round(total_unrealized_pl, 2),
        "holdings": holdings_data,
    }


def buy_real_asset(symbol, quantity, db):
    if quantity <= 0:
        return {"error": "Quantity must be greater than zero"}

    symbol = symbol.upper()
    quote = get_quote(symbol)

    if "error" in quote:
        return quote

    portfolio = get_or_create_real_portfolio(db)

    price = quote["price"]
    total_cost = round(price * quantity, 2)

    if portfolio.cash < total_cost:
        return {"error": "Not enough cash"}

    portfolio.cash = round(portfolio.cash - total_cost, 2)

    holding = db.query(RealHolding).filter(
        RealHolding.symbol == symbol
    ).first()

    if holding:
        old_total = holding.quantity * holding.average_price
        new_total = quantity * price
        new_quantity = holding.quantity + quantity

        holding.quantity = new_quantity
        holding.average_price = round((old_total + new_total) / new_quantity, 2)
    else:
        holding = RealHolding(
            symbol=symbol,
            name=quote["name"],
            asset_class=quote["asset_class"],
            sector=quote["sector"],
            quantity=quantity,
            average_price=price,
        )
        db.add(holding)

    transaction = RealTransaction(
        symbol=symbol,
        name=quote["name"],
        trade_type="BUY",
        quantity=quantity,
        price=price,
        total_value=total_cost,
    )

    db.add(transaction)
    db.commit()

    return {
        "message": "Real-market buy order successful",
        "portfolio": get_real_portfolio(db),
    }


def sell_real_asset(symbol, quantity, db):
    if quantity <= 0:
        return {"error": "Quantity must be greater than zero"}

    symbol = symbol.upper()
    quote = get_quote(symbol)

    if "error" in quote:
        return quote

    holding = db.query(RealHolding).filter(
        RealHolding.symbol == symbol
    ).first()

    if not holding:
        return {"error": "You do not own this asset"}

    if holding.quantity < quantity:
        return {"error": "Not enough quantity to sell"}

    portfolio = get_or_create_real_portfolio(db)

    price = quote["price"]
    sale_value = round(price * quantity, 2)

    portfolio.cash = round(portfolio.cash + sale_value, 2)
    holding.quantity -= quantity

    if holding.quantity == 0:
        db.delete(holding)

    transaction = RealTransaction(
        symbol=symbol,
        name=quote["name"],
        trade_type="SELL",
        quantity=quantity,
        price=price,
        total_value=sale_value,
    )

    db.add(transaction)
    db.commit()

    return {
        "message": "Real-market sell order successful",
        "portfolio": get_real_portfolio(db),
    }


def get_real_transactions(db):
    transactions = db.query(RealTransaction).order_by(
        RealTransaction.timestamp.desc()
    ).all()

    return [
        {
            "id": transaction.id,
            "symbol": transaction.symbol,
            "name": transaction.name,
            "trade_type": transaction.trade_type,
            "quantity": transaction.quantity,
            "price": transaction.price,
            "total_value": transaction.total_value,
            "timestamp": transaction.timestamp,
        }
        for transaction in transactions
    ]


def reset_real_portfolio(db):
    db.query(RealHolding).delete()
    db.query(RealTransaction).delete()

    portfolio = get_or_create_real_portfolio(db)
    portfolio.cash = 10000.0

    db.commit()

    return {"message": "Real-market portfolio reset successfully"}