import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

MAX_RETRIES = 10
WAIT_SECONDS = 2

engine = None

for attempt in range(1, MAX_RETRIES + 1):
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(" Database connection established")
        break
    except OperationalError:
        print(f" Database not ready (attempt {attempt}/{MAX_RETRIES})")
        time.sleep(WAIT_SECONDS)
else:
    raise RuntimeError(" Database not available after retries")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
