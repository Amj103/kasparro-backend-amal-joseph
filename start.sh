#!/bin/sh

echo "Running ETL..."
python -m ingestion.runner

echo "Starting API..."
uvicorn api.main:app --host 0.0.0.0 --port 8000
