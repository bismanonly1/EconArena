from database import Base, engine, SessionLocal
from db_models import Asset, Portfolio


def init_database():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    existing_assets = db.query(Asset).count()

    if existing_assets == 0:
        starter_assets = [
            Asset(name="TechNova", sector="Technology", price=100.0, volatility=0.08),
            Asset(name="EnergyMax", sector="Energy", price=80.0, volatility=0.10),
            Asset(name="HealthCore", sector="Healthcare", price=60.0, volatility=0.05),
            Asset(name="BankTrust", sector="Banking", price=90.0, volatility=0.07),
            Asset(name="DefenseShield", sector="Defense", price=110.0, volatility=0.09),
        ]

        db.add_all(starter_assets)

    existing_portfolio = db.query(Portfolio).count()

    if existing_portfolio == 0:
        db.add(Portfolio(cash=10000.0))

    db.commit()
    db.close()


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")