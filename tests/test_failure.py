import pytest
from ingestion.csv_ingestion import ingest_csv
from api.db import SessionLocal
from api.models import ETLCheckpoint

def test_etl_failure():
    db = SessionLocal()

    try:
        
        db.query(ETLCheckpoint).filter_by(source_name="csv").delete()
        db.commit()

        with pytest.raises(Exception):
            ingest_csv(db, "data/non_existent.csv")
            
    finally:
        db.close()