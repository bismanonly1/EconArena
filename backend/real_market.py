import yfinance as yf

from canadian_universe import get_asset_by_symbol


def get_quote(symbol):
    symbol = symbol.upper()
    asset = get_asset_by_symbol(symbol)

    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1mo", interval="1d")

        if history.empty:
            return {
                "error": f"No market data found for {symbol}"
            }

        latest_row = history.iloc[-1]

        if len(history) >= 2:
            previous_row = history.iloc[-2]
        else:
            previous_row = latest_row

        latest_price = round(float(latest_row["Close"]), 2)
        previous_close = round(float(previous_row["Close"]), 2)

        change = round(latest_price - previous_close, 2)

        if previous_close != 0:
            change_percent = round((change / previous_close) * 100, 2)
        else:
            change_percent = 0

        return {
            "symbol": symbol,
            "name": asset["name"] if asset else symbol,
            "asset_class": asset["asset_class"] if asset else "Unknown",
            "sector": asset["sector"] if asset else "Unknown",
            "risk_level": asset["risk_level"] if asset else "Unknown",
            "price": latest_price,
            "previous_close": previous_close,
            "change": change,
            "change_percent": change_percent,
            "currency": "CAD",
        }

    except Exception as error:
        return {
            "error": f"Failed to fetch quote for {symbol}",
            "details": str(error)
        }


def get_quotes(symbols):
    quotes = []

    for symbol in symbols:
        quote = get_quote(symbol)

        if "error" not in quote:
            quotes.append(quote)

    return quotes


def get_price_history(symbol, period="1mo", interval="1d"):
    symbol = symbol.upper()

    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=period, interval=interval)

        if history.empty:
            return {
                "error": f"No historical market data found for {symbol}"
            }

        records = []

        for index, row in history.iterrows():
            records.append({
                "date": index.strftime("%Y-%m-%d"),
                "open": round(float(row["Open"]), 2),
                "high": round(float(row["High"]), 2),
                "low": round(float(row["Low"]), 2),
                "close": round(float(row["Close"]), 2),
                "volume": int(row["Volume"]),
            })

        return {
            "symbol": symbol,
            "history": records,
        }

    except Exception as error:
        return {
            "error": f"Failed to fetch historical data for {symbol}",
            "details": str(error)
        }