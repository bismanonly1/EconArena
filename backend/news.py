import random

news_templates = [
    {
        "title": "AI breakthrough boosts technology sector confidence",
        "sector": "Technology",
        "sentiment": "positive",
        "severity": 0.08
    },
    {
        "title": "Oil supply disruption increases energy prices",
        "sector": "Energy",
        "sentiment": "positive",
        "severity": 0.10
    },
    {
        "title": "New banking regulations pressure financial stocks",
        "sector": "Banking",
        "sentiment": "negative",
        "severity": 0.07
    },
    {
        "title": "Global health innovation improves healthcare outlook",
        "sector": "Healthcare",
        "sentiment": "positive",
        "severity": 0.05
    },
    {
        "title": "Geopolitical tension increases defense spending expectations",
        "sector": "Defense",
        "sentiment": "positive",
        "severity": 0.09
    }
]

def generate_news():
    return random.choice(news_templates)