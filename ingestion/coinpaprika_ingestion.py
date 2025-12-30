import requests
from datetime import datetime

from api.db import SessionLocal
from api.models import Asset, AssetMetric


TICKERS_URL = "https://api.coinpaprika.com/v1/tickers"
LIMIT = 10  


def run_coinpaprika_ingestion():
    db = SessionLocal()
    records = 0

    try:
        response = requests.get(TICKERS_URL, timeout=10)
        response.raise_for_status()

        data = response.json()[:LIMIT]

        for item in data:
            symbol = item["symbol"]
            name = item["name"]
            price = item["quotes"]["USD"]["price"]

            asset = db.query(Asset).filter_by(symbol=symbol).first()
            if not asset:
                asset = Asset(symbol=symbol, name=name)
                db.add(asset)
                db.flush()

            metric = AssetMetric(
                asset_id=asset.id,
                source="coinpaprika",
                value=float(price),
                event_time=datetime.utcnow(),
            )

            db.add(metric)
            records += 1

        db.commit()
        print(f" CoinPaprika ingestion completed ({records} records)")
        return records  

    except Exception as e:
        db.rollback()
        print(" CoinPaprika ingestion failed:", e)
        raise

    finally:
        db.close()
