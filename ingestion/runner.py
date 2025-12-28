from api.db import SessionLocal
from ingestion.csv_ingestion import ingest_csv
from ingestion.coinpaprika_ingestion import ingest_coinpaprika
from ingestion.coingecko_ingestion import ingest_coingecko
from api.models import ETLRun
from datetime import datetime


def run_etl():
    db = SessionLocal()

    run = ETLRun(
        started_at=datetime.utcnow(),
        status="running",
        records_processed=0
    )
    db.add(run)
    db.commit()

    try:
        records = 0

        records += ingest_csv(db, "data/sample.csv")
        records += ingest_coinpaprika(db)
        records += ingest_coingecko(db)

        run.status = "success"
        run.records_processed = records

    except Exception as e:
        run.status = "failed"
        run.error_message = str(e)

    finally:
        run.ended_at = datetime.utcnow()
        db.commit()
        db.close()


if __name__ == "__main__":
    run_etl()
