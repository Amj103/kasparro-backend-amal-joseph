from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models import Base
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL")

for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        break
    except Exception:
        print(f"DB not ready, retrying ({i+1}/10)...")
        time.sleep(2)
else:
    raise Exception("Database not available")

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
