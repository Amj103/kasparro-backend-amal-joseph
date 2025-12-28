import csv
from sqlalchemy.orm import Session
from api.models import RawCSVData, NormalizedData, ETLCheckpoint

SOURCE_NAME = "csv"


def ingest_csv(db: Session, file_path: str):
    checkpoint = db.get(ETLCheckpoint, SOURCE_NAME)
    last_id = checkpoint.last_processed_id if checkpoint else 0
    processed = 0

    with open(file_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_id = int(row["id"])
            if row_id <= last_id:
                continue

            # raw storage
            raw = RawCSVData(
                id=row_id,
                payload=row
            )
            db.merge(raw)

            # normalized storage
            normalized = NormalizedData(
                source=SOURCE_NAME,
                external_id=row_id,
                name=row["name"],
                value=row["value"],
                event_time=row["event_time"]
            )
            db.merge(normalized)

            last_id = row_id
            processed += 1

    if checkpoint:
        checkpoint.last_processed_id = last_id
    else:
        checkpoint = ETLCheckpoint(
            source_name=SOURCE_NAME,
            last_processed_id=last_id
        )
        db.add(checkpoint)

    db.commit()
    return processed
