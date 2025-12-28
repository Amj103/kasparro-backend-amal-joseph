from ingestion.csv_ingestion import ingest_csv
from api.db import SessionLocal
from api.models import ETLCheckpoint

def test_csv_etl_incremental():
    db = SessionLocal()

    
    count1 = ingest_csv(db, "data/sample.csv")
    assert count1 >= 0

   
    count2 = ingest_csv(db, "data/sample.csv")
    assert count2 == 0

    checkpoint = db.get(ETLCheckpoint, "csv")
    assert checkpoint is not None

    db.close()
