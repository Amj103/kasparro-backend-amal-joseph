import csv
from datetime import datetime

from api.db import SessionLocal
from api.models import Asset, AssetMetric


CSV_PATH = "data/sample.csv"


def run_csv_ingestion():
    db = SessionLocal()
    records = 0

    try:
        with open(CSV_PATH, newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                symbol = row["symbol"].strip().upper()
                name = row["name"].strip()
                value = float(row["price"])

                # Check if asset exists
                asset = db.query(Asset).filter_by(symbol=symbol).first()

                if not asset:
                    asset = Asset(symbol=symbol, name=name)
                    db.add(asset)
                    db.flush()  # get asset.id

                metric = AssetMetric(
                    asset_id=asset.id,
                    source="csv",
                    value=value,
                    event_time=datetime.utcnow(),
                )

                db.add(metric)
                records += 1

        db.commit()
        print(f" CSV ingestion completed ({records} records)")
        return records

    except Exception as e:
        db.rollback()
        print(" CSV ingestion failed:", e)
        raise

    finally:
        db.close()
