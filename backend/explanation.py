def explain_market_event(news_event):
    sector = news_event["sector"]
    sentiment = news_event["sentiment"]
    severity = news_event["severity"]
    title = news_event["title"]

    direction = "increased" if sentiment == "positive" else "decreased"

    return {
        "headline": title,
        "explanation": f"The {sector} sector {direction} because the news event created {sentiment} sentiment. The severity score was {severity}, so prices moved by approximately {round(severity * 100, 2)}%.",
        "learning_point": f"This shows how {sector} assets can react to news, sentiment, and perceived economic impact."
    }