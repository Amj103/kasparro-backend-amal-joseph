from fastapi import FastAPI, Query
import time, uuid
from sqlalchemy import text
from api.db import engine, SessionLocal
from api.models import Base, ETLRun  # Ensure ETLRun is imported
from api.data_service import get_data

app = FastAPI()

@app.on_event("startup")
def startup():
    # Ensures all tables are created upon startup
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    db = SessionLocal()
    start_time = time.time()
    try:
        db.execute(text("SELECT 1"))
        # Reports ETL last-run status (P0.2 Requirement)
        last_run = db.query(ETLRun).order_by(ETLRun.started_at.desc()).first()
        return {
            "status": "ok",
            "request_id": str(uuid.uuid4()),
            "api_latency_ms": int((time.time() - start_time) * 1000),
            "database": "connected",
            "last_etl_run": {
                "status": last_run.status if last_run else "no_runs_yet",
                "timestamp": last_run.ended_at if last_run else None
            }
        }
    finally:
        db.close()

@app.get("/data")
def data_api(
    source: str | None = Query(default=None),
    limit: int = 10,
    offset: int = 0,
):
    start_time = time.time()
    db = SessionLocal()
    try:
        total, data = get_data(db, source, limit, offset)
        return {
            "request_id": str(uuid.uuid4()),
            "api_latency_ms": int((time.time() - start_time) * 1000),
            "total": total,
            "data": data
        }
    finally:
        db.close()

@app.get("/stats")
def etl_stats():
    db = SessionLocal()
    try:
        # P1.3 Requirement: Expose ETL summaries
        runs = db.query(ETLRun).order_by(ETLRun.started_at.desc()).limit(10).all()
        return {
            "runs": [
                {
                    "run_id": r.id,
                    "status": r.status,
                    "started_at": r.started_at,
                    "ended_at": r.ended_at,
                    "records_processed": r.records_processed,
                    "error_message": r.error_message
                } for r in runs
            ]
        }
    finally:
        db.close()