📌 Architecture Overview



The system ingests data from multiple sources, normalizes it into a unified schema, exposes query APIs, and runs fully containerized with automated testing and cloud deployment.



High-Level Flow

CSV / APIs (CoinPaprika, CoinGecko)

&nbsp;       ↓

&nbsp;  Raw Tables (Postgres)

&nbsp;       ↓

&nbsp;Normalized Unified Schema

&nbsp;       ↓

&nbsp;  FastAPI Backend

&nbsp;       ↓

&nbsp;Public API Endpoints



🗂️ Project Structure

.

├── api/                    # FastAPI application

│   ├── main.py             # API entry point

│   ├── db.py               # DB session \& engine

│   ├── models.py           # SQLAlchemy models

│   └── services.py         # Data access logic

│

├── ingestion/              # ETL pipelines

│   ├── runner.py           # ETL orchestrator

│   ├── csv\_ingestion.py    # CSV ingestion

│   ├── coinpaprika\_ingestion.py

│   └── coingecko\_ingestion.py

│

├── data/

│   └── sample.csv          # CSV source

│

├── tests/                  # Test suite

│   ├── test\_api.py

│   ├── test\_etl.py

│   └── test\_failure.py

│

├── docker-compose.yml

├── Dockerfile

├── start.sh                # Startup script (ETL + API)

├── requirements.txt

├── pytest.ini

├── .github/workflows/ci.yml

└── README.md



⚙️ Tech Stack



Python 3.11



FastAPI



PostgreSQL



SQLAlchemy



Docker \& Docker Compose



GitHub Actions (CI)



AWS EC2 (Deployment)



🔄 Data Ingestion (ETL)

Sources



CSV (data/sample.csv)



CoinPaprika API



CoinGecko API



Features



Raw data stored in raw\_\* tables



Normalized unified schema



Type validation



Incremental ingestion (no reprocessing)



Idempotent writes



Resume-on-failure logic



Run metadata stored in etl\_runs



Execution



ETL runs:



Automatically on container startup



On-demand via:



docker-compose run --rm api python -m ingestion.runner





Hourly via cron on EC2



🌐 API Endpoints

GET /health



Health check endpoint.



Returns:



Database connectivity



Last ETL run status



{

&nbsp; "status": "ok",

&nbsp; "db": "connected"

}



GET /data



Fetch normalized data.



Features



Pagination



Filtering



Metadata included



Example:



{

&nbsp; "request\_id": "...",

&nbsp; "api\_latency\_ms": 12,

&nbsp; "pagination": {

&nbsp;   "limit": 10,

&nbsp;   "offset": 0,

&nbsp;   "total": 12240

&nbsp; },

&nbsp; "data": \[...]

}



GET /stats



ETL run statistics.



Returns:



Records processed



Duration



Last success \& failure timestamps



Run metadata



GET /metrics



Prometheus-style metrics.



Example:



etl\_last\_run\_success 1

etl\_records\_total 12240

api\_status 1



🐳 Dockerized System



The entire system runs via Docker.



Build \& Run

docker-compose up --build



Stop

docker-compose down



🧪 Testing



Tests run inside Docker, matching production.



Run Tests

docker-compose run --rm api pytest



Coverage



ETL transformations



Incremental ingestion



Failure recovery



API endpoints



🔁 CI/CD Pipeline (P2)



GitHub Actions automatically runs on:



Push



Pull Request



CI Steps



Checkout code



Build Docker images



Run test suite inside containers



CI config:



.github/workflows/ci.yml





✅ All tests must pass for CI to succeed



☁️ Cloud Deployment (AWS EC2)



Deployed on AWS EC2 (Ubuntu)



Docker + Docker Compose installed



Public API exposed



Scheduled ETL via cron



Cron Job



Runs ETL hourly:



0 \* \* \* \* cd /home/ubuntu/kasparro-backend-amal-joseph \&\& docker-compose run --rm api python -m ingestion.runner >> etl.log 2>\&1



🔐 Secrets Management



API keys stored using environment variables



No secrets committed to source control



Docker .env supported

