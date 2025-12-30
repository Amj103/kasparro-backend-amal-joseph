from fastapi import FastAPI, Query
import time, uuid
from api.db import engine, SessionLocal
from api.models import Base
from api.data_service import get_data

app = FastAPI()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/data")
def data_api(
    source: str | None = Query(default=None),
    limit: int = 10,
    offset: int = 0,
):
    db = SessionLocal()
    try:
        total, data = get_data(db, source, limit, offset)
        return {
            "request_id": str(uuid.uuid4()),
            "total": total,
            "data": data
        }
    finally:
        db.close()
