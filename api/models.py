from sqlalchemy import Column, Integer, BigInteger, String, JSON, TIMESTAMP, Numeric, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Text
import uuid

Base = declarative_base()

class RawCSVData(Base):
    __tablename__ = "raw_csv_data"

    id = Column(BigInteger, primary_key=True)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(TIMESTAMP, server_default=func.now())


class NormalizedData(Base):
    __tablename__ = "normalized_data"

    id = Column(Integer, primary_key=True)
    source = Column(String(50), nullable=False)
    external_id = Column(BigInteger, nullable=False)
    name = Column(String)
    value = Column(Numeric)
    event_time = Column(TIMESTAMP)

    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_source_external"),
    )


class ETLCheckpoint(Base):
    __tablename__ = "etl_checkpoints"

    source_name = Column(String(50), primary_key=True)
    last_processed_id = Column(BigInteger, nullable=False)

class ETLRun(Base):
    __tablename__ = "etl_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    status = Column(String(20))  # success / failed
    records_processed = Column(Integer)
    error_message = Column(Text)

class RawCoinPaprika(Base):
    __tablename__ = "raw_coinpaprika"

    id = Column(String, primary_key=True)
    payload = Column(JSON, nullable=False)
    ingested_at = Column(TIMESTAMP, server_default=func.now())
