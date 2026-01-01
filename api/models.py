from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base = declarative_base()

class Asset(Base):
    __tablename__ = "assets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    symbol = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    sources = relationship("AssetSourceMap", back_populates="asset")
    metrics = relationship("AssetMetric", back_populates="asset")

class AssetSourceMap(Base):
    __tablename__ = "asset_source_map"
    id = Column(Integer, primary_key=True)
    asset_id = Column(String, ForeignKey("assets.id"), nullable=False)
    source = Column(String, nullable=False)
    external_id = Column(String, nullable=False)
    asset = relationship("Asset", back_populates="sources")

class AssetMetric(Base):
    __tablename__ = "asset_metrics"
    id = Column(Integer, primary_key=True)
    asset_id = Column(String, ForeignKey("assets.id"), nullable=False)
    source = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    event_time = Column(DateTime, default=datetime.utcnow)
    asset = relationship("Asset", back_populates="metrics")

class ETLCheckpoint(Base):
    __tablename__ = "etl_checkpoints"
    source_name = Column(String, primary_key=True)
    last_processed_key = Column(String, nullable=False)

class ETLRun(Base):
    __tablename__ = "etl_runs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime)
    status = Column(String, nullable=False)
    records_processed = Column(Integer, default=0, nullable=False)
    error_message = Column(String)