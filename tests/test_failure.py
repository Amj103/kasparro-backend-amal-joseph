from ingestion.csv_ingestion import ingest_csv
from api.db import SessionLocal
import pytest

def test_etl_failure():
    db = SessionLocal()

    with pytest.raises(Exception):
        ingest_csv(db, "data/non_existent.csv")

    db.close()
