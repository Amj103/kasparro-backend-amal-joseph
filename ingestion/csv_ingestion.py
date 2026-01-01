import csv
from datetime import datetime
from api.db import SessionLocal
from api.models import Asset, AssetMetric, ETLCheckpoint

CSV_PATH = "data/sample.csv"

def ingest_csv(db, file_path=CSV_PATH):
    records = 0
    try:
        # P1.2 Requirement: Incremental Ingestion via Checkpoint
        checkpoint = db.query(ETLCheckpoint).filter_by(source_name="csv").first()
        if checkpoint and checkpoint.last_processed_key == "DONE":
            print(f" CSV ingestion skipped: {file_path} already processed.")
            return 0

        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                symbol = row["symbol"].strip().upper()
                name = row["name"].strip()
                value = float(row["price"])

                asset = db.query(Asset).filter_by(symbol=symbol).first()
                if not asset:
                    asset = Asset(symbol=symbol, name=name)
                    db.add(asset)
                    db.flush()

                metric = AssetMetric(
                    asset_id=asset.id,
                    source="csv",
                    value=value,
                    event_time=datetime.utcnow(),
                )
                db.add(metric)
                records += 1

        # Update Checkpoint
        if not checkpoint:
            checkpoint = ETLCheckpoint(source_name="csv", last_processed_key="DONE")
            db.add(checkpoint)
        else:
            checkpoint.last_processed_key = "DONE"

        db.commit()
        print(f" CSV ingestion completed ({records} records)")
        return records

    except Exception as e:
        db.rollback()
        print(" CSV ingestion failed:", e)
        raise

def run_csv_ingestion():
    db = SessionLocal()
    try:
        return ingest_csv(db)
    finally:
        db.close()