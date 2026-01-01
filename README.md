Project K: Unified Crypto ETL & API Pipeline

A production-grade, containerized ETL (Extract, Transform, Load) pipeline and FastAPI application. This project automates the ingestion of cryptocurrency data from multiple sources into a unified PostgreSQL schema, deployed on AWS EC2 via a custom CI/CD pipeline.

🚀 Live Cloud Deployment

The system is currently live and operational on AWS EC2.

Base API URL: http://15.134.212.133:8000

Health Status: http://15.134.212.133:8000/health

Dynamic Metrics: http://15.134.212.133:8000/metrics

Data Explorer: http://15.134.212.133:8000/data

🏗️ Architecture & Design

The system is designed with a modular approach to separate data ingestion from consumption, ensuring scalability and fault tolerance.

1. Ingestion Layer (ETL)

The ETL pipeline is built in Python and handles the complexity of interfacing with diverse data sources:

CSV Ingestion: Processes local data files using a checkpointing system (ETLCheckpoint) to skip already processed files.

External APIs: Integrated with CoinGecko and CoinPaprika. It handles data normalization, converting disparate JSON structures into a unified internal model.

2. Storage Layer

Uses a PostgreSQL database managed via SQLAlchemy ORM.

Unified Schema: All assets are mapped to a single AssetMetric table, allowing for cross-source analysis.

Auditability: The ETLRun table tracks the metadata of every pipeline execution (duration, record count, success/failure).

3. API Layer

A FastAPI application serves the ingested data. It includes pagination for the /data endpoint and custom observability logic for /metrics.

4. DevOps & Cloud

Containerization: Entire stack is orchestrated with Docker Compose.

CI/CD: GitHub Actions automates testing (Pytest) and secure deployment via SSH.

🛠️ Local Setup

1. Clone the repository

git clone [https://github.com/Amj103/kasparro-backend-amal-joseph.git](https://github.com/Amj103/kasparro-backend-amal-joseph.git)
cd kasparro-backend-amal-joseph


2. Environment Configuration

Create a .env file in the project root:

POSTGRES_USER=kasparro
POSTGRES_PASSWORD=kasparro
POSTGRES_DB=kasparro_db
DATABASE_URL=postgresql://kasparro:kasparro@db:5432/kasparro_db


3. Launch Services

# Build images and start containers in detached mode
docker-compose up --build -d


4. Running Tests

# Run the test suite inside the API container
docker-compose run --rm api pytest


🛠️ Features implemented (P-Level)

P0.3/P2.3: Full Dockerization and Cloud Deployment on AWS.

P1.1: Multi-source ETL (CSV + 2 External APIs).

P1.2: Incremental ingestion logic using ETLCheckpoint.

P2.4: Observability layer with dynamic /metrics endpoint.

P1.4: Comprehensive testing suite including API health and failure scenarios.

⚙️ CI/CD Workflow

The deployment is fully automated. On every push to main:

Test Job: GitHub Actions spins up a temporary environment, builds the image, and runs the test suite.

Deploy Job: Upon successful tests, it uses SSH to connect to 15.134.212.133, pulls the latest code, and restarts the containers using docker-compose up --build -d.

📊 Sample ETL Output

Starting ETL pipeline
Database connection established
Database schema ensured
Running CSV ingestion
CSV ingestion completed (5 records)
Running CoinGecko ingestion
CoinGecko ingestion completed (5 records)
Running CoinPaprika ingestion
CoinPaprika ingestion completed (10 records)
ETL completed successfully (20 records)
