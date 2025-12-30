import requests
from datetime import datetime

from api.db import SessionLocal
from api.models import Asset, AssetMetric


COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
COINS = ["bitcoin", "ethereum", "binancecoin", "ripple", "tether"]
VS_CURRENCY = "usd"


def run_coingecko_ingestion():
    db = SessionLocal()
    records = 0

    try:
        response = requests.get(
            COINGECKO_URL,
            params={
                "ids": ",".join(COINS),
                "vs_currencies": VS_CURRENCY,
            },
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()

        for coin_id, price_data in data.items():
            symbol = coin_id.upper()
            value = float(price_data[VS_CURRENCY])

            asset = db.query(Asset).filter_by(symbol=symbol).first()
            if not asset:
                asset = Asset(symbol=symbol, name=coin_id.capitalize())
                db.add(asset)
                db.flush()

            metric = AssetMetric(
                asset_id=asset.id,
                source="coingecko",
                value=value,
                event_time=datetime.utcnow(),
            )

            db.add(metric)
            records += 1

        db.commit()
        print(f" CoinGecko ingestion completed ({records} records)")
        return records  

    except Exception as e:
        db.rollback()
        print(" CoinGecko ingestion failed:", e)
        raise

    finally:
        db.close()
