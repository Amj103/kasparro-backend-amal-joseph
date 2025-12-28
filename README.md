📌 Architecture Overview



The system follows a standard ETL (Extract, Transform, Load) pattern to ensure data integrity and high availability.



High-Level Data Flow



Extraction: Ingests data from CSV files and external REST APIs.



Raw Storage: Data is first landed in raw\_\* tables in PostgreSQL.



Transformation: Normalizes disparate data formats into a Unified Schema.



Exhibition: A FastAPI application serves the normalized data via public endpoints.



graph TD

&nbsp;   A\[CSV Source] --> D\[PostgreSQL Raw Tables]

&nbsp;   B\[CoinPaprika API] --> D

&nbsp;   C\[CoinGecko API] --> D

&nbsp;   D --> E{Normalization Engine}

&nbsp;   E --> F\[Unified Schema]

&nbsp;   F --> G\[FastAPI Backend]

&nbsp;   G --> H\[Public API Endpoints]





⚙️ Tech Stack



Language: Python 3.11



Framework: FastAPI



Database: PostgreSQL + SQLAlchemy (ORM)



Infrastructure: Docker \& Docker Compose



CI/CD: GitHub Actions



Cloud: AWS EC2 (Ubuntu)



🗂️ Project Structure



.

├── api/                    # FastAPI application

│   ├── main.py             # API entry point

│   ├── db.py               # DB session \& engine

│   ├── models.py           # SQLAlchemy models

│   └── services.py         # Data access logic

├── ingestion/              # ETL pipelines

│   ├── runner.py           # ETL orchestrator

│   ├── csv\_ingestion.py    # CSV ingestion logic

│   ├── coinpaprika\_ingestion.py

│   └── coingecko\_ingestion.py

├── data/

│   └── sample.csv          # Local data source

├── tests/                  # Pytest suite

│   ├── test\_api.py

│   ├── test\_etl.py

│   └── test\_failure.py

├── docker-compose.yml      # Orchestration

├── Dockerfile              # Backend container definition

├── start.sh                # Startup script (ETL + API)

├── requirements.txt        # Python dependencies

└── .github/workflows/ci.yml # GitHub Actions config





🔄 Data Ingestion (ETL)



The ETL engine is built for reliability and scale.



Key Features



Incremental Ingestion: Skips already processed data to save resources.



Idempotency: Multiple runs produce the same state without duplicates.



Resume-on-failure: Logic to pick up where it left off after an interruption.



Metadata Tracking: Every run status is logged in the etl\_runs table.



Execution



The ETL runs automatically on container startup. To trigger it manually:



docker-compose run --rm api python -m ingestion.runner





🌐 API Endpoints



Endpoint



Method



Description



/health



GET



System health, DB connection, and last ETL status.



/data



GET



Paginated and filtered access to normalized crypto data.



/stats



GET



Statistics on records processed and ETL run durations.



/metrics



GET



Prometheus-style metrics for monitoring.



🐳 Getting Started (Docker)



Build and Run



docker-compose up --build





Running Tests



Tests run inside the container to ensure environment parity:



docker-compose run --rm api pytest





☁️ Deployment \& CI/CD



GitHub Actions (CI)



On every Push or Pull Request, the system:



Builds the Docker images.



Spins up a temporary Postgres instance.



Runs the full test suite (API, ETL, and Failure Recovery).



AWS EC2 Deployment



The system is deployed on an Ubuntu EC2 instance. The ETL is scheduled via cron to run hourly:



0 \* \* \* \* cd /home/ubuntu/project-root \&\& docker-compose run --rm api python -m ingestion.runner >> etl.log 2>\&1





🔐 Secrets Management



API keys and database credentials are managed via environment variables.



Use a .env file for local development (not committed to version control).



Production secrets are managed via GitHub Secrets or AWS Parameter Store.

