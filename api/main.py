from fastapi import FastAPI, Query
import time, uuid
from sqlalchemy import text
from api.db import engine, SessionLocal
from api.models import Base
from api.data_service import get_data
from api.models import ETLRun


app = FastAPI()

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    start = time.time()
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "db": db_status,
        "request_id": str(uuid.uuid4()),
        "api_latency_ms": int((time.time() - start) * 1000)
    }

@app.get("/data")
def get_data_api(
    source: str | None = Query(default=None),
    limit: int = Query(default=10, le=100),
    offset: int = Query(default=0),
):
    start = time.time()
    request_id = str(uuid.uuid4())

    db = SessionLocal()
    try:
        total, rows = get_data(
            db=db,
            source=source,
            limit=limit,
            offset=offset
        )

        data = [
            {
                "id": r.id,
                "source": r.source,
                "external_id": r.external_id,
                "name": r.name,
                "value": float(r.value) if r.value is not None else None,
                "event_time": r.event_time,
            }
            for r in rows
        ]

        return {
            "request_id": request_id,
            "api_latency_ms": int((time.time() - start) * 1000),
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": total
            },
            "data": data
        }
    finally:
        db.close()

@app.get("/stats")
def etl_stats():
    start = time.time()
    request_id = str(uuid.uuid4())

    db = SessionLocal()
    try:
        runs = (
            db.query(ETLRun)
            .order_by(ETLRun.started_at.desc())
            .limit(5)
            .all()
        )

        data = [
            {
                "run_id": r.id,
                "status": r.status,
                "started_at": r.started_at,
                "ended_at": r.ended_at,
                "records_processed": r.records_processed,
                "error": r.error_message,
            }
            for r in runs
        ]

        return {
            "request_id": request_id,
            "api_latency_ms": int((time.time() - start) * 1000),
            "runs": data
        }
    finally:
        db.close()
