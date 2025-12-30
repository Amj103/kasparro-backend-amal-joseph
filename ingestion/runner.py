import time
from datetime import datetime

from sqlalchemy import text

from api.db import SessionLocal, engine
from api.models import ETLRun, Base

from ingestion.csv_ingestion import run_csv_ingestion
from ingestion.coingecko_ingestion import run_coingecko_ingestion
from ingestion.coinpaprika_ingestion import run_coinpaprika_ingestion


MAX_RETRIES = 15
SLEEP_SECONDS = 2


def wait_for_db():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(" Database connection established")
            return
        except Exception:
            print(f" Database not ready (attempt {attempt}/{MAX_RETRIES})")
            time.sleep(SLEEP_SECONDS)

    raise RuntimeError("Database never became ready")


def run_etl():
    print(" Starting ETL pipeline")

    # 1️⃣ Wait for DB
    wait_for_db()

    # 2️⃣ CREATE ALL TABLES (CRITICAL FIX)
    Base.metadata.create_all(bind=engine)
    print("Database schema ensured")

    db = SessionLocal()

    etl_run = ETLRun(
        status="running",
        started_at=datetime.utcnow(),
        records_processed=0,
    )

    try:
        # 3️⃣ Insert ETL run start
        db.add(etl_run)
        db.commit()
        db.refresh(etl_run)

        total_records = 0

        # 4️⃣ Run ingestions
        print(" Running CSV ingestion")
        total_records += run_csv_ingestion()

        print(" Running CoinGecko ingestion")
        total_records += run_coingecko_ingestion()

        print(" Running CoinPaprika ingestion")
        total_records += run_coinpaprika_ingestion()

        # 5️⃣ Mark success
        etl_run.status = "success"
        etl_run.records_processed = total_records
        etl_run.ended_at = datetime.utcnow()

        db.commit()
        print(f" ETL completed successfully ({total_records} records)")

    except Exception as e:
        db.rollback()

        # 6️⃣ Mark failure safely
        etl_run.status = "failure"
        etl_run.error_message = str(e)
        etl_run.ended_at = datetime.utcnow()

        db.commit()
        print(" ETL failed:", e)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    run_etl()
