# Earth(Seoul) Monitoring System

A data pipeline for collecting, processing, and visualizing environmental data from multiple sources.

<img width="858" alt="Image" src="https://github.com/user-attachments/assets/79f270e9-ed33-4174-89d8-2c7a47f716a4" />

## Presentation

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/iWE8yVl6ryE/0.jpg)](https://www.youtube.com/watch?v=iWE8yVl6ryE)

## Project Overview

The Earth(Seoul) Monitoring System is a comprehensive data pipeline designed to:

1. Collect environmental data from multiple sources (air quality, climate data)
2. Process and transform the data
3. Orchestrate workflows with Apache Airflow
4. Visualize the results with Tableau (including advanced interactive dashboards)

## Visualization

Check Tableau Desktop file and database under **Tableau Desktop Files**

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Tableau Desktop (for visualization)

## Directory Structure

```
earth-monitoring-system/
├── airflow/
│   ├── dags/             # Airflow DAG definitions
│   ├── logs/             # Airflow logs
│   └── config/           # Airflow configuration
├── infrastructure/
│   └── postgres/
│       └── init.sql      # PostgreSQL initialization script
├── kaggle_data_source/   # Raw data (gitignored)
│   ├── AirPollutionSeoul # unzip air seoul air polution data from Kaggle
│   └── SeoulHistoricalWeatehrData # unzip seoul historical weather data
├── docker-compose.yml    # Docker Compose configuration
└── README.md
```

## Data Sources

- [Air Pollution in Seoul (Kaggle)](https://www.kaggle.com/datasets/bappekim/air-pollution-in-seoul)
- [Seoul Historical Weather Data 2024 (Kaggle)](https://www.kaggle.com/datasets/alfredkondoro/seoul-historical-weather-data-2024)

**Check Directory Structure and put the data source in the right folder**


## Usage Quick Reference

1. **Clone and start services:**
   ```bash
   git clone <repository-url>
   cd earth-monitoring-system
   docker compose up -d
   ```
2. **Initialize Airflow (first time):**
   ```bash
   docker compose run airflow-webserver airflow db init
   docker compose run airflow-webserver airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
   ```
3. **Access Airflow UI:**
   - Go to http://localhost:8080 (admin/admin)
4. **Run ingestion and transformation DAG:**
   - Trigger manually from the Airflow UI.
   - Monitor logs for task success.
5. **Connect Tableau or psql to Postgres:**
   - Host: localhost
   - Port: 5432
   - Database: earth_monitoring
   - Username: postgres
   - Password: postgres
6. **Tableau Dashboard:**
   - Open Tableau, connect to the processed/clean tables.
   - Explore dashboards: scatter plots, seasonal trends, and interactive features 

## Progress & Milestones

### Completed
- **Environment setup**: Docker Compose with Airflow, Postgres, and volume mounts for local and containerized development.
- **Python requirements**: Version-pinned to ensure pandas, sqlalchemy, and psycopg2-binary compatibility (see `airflow/requirements.txt`).
- **Airflow connection**: Configured via Airflow UI and `docker-compose.yml` with `DATA_PREFIX` for robust CSV path resolution.
- **Data ingestion**: Python scripts and Airflow DAGs load and clean Kaggle CSV data into Postgres staging tables using pandas and SQLAlchemy.
- **Testing**: Ingestion scripts tested both locally and in Dockerized Airflow, verified with manual queries and Airflow logs.
- **SQL transformation**: Created and tested `transform_seoul_data.sql` to produce a clean, analysis-ready table in Postgres.
- **Airflow transformation task**: Added a PostgresOperator step to automate SQL transformation in the DAG and verified end-to-end orchestration.
- **Visualization**: Connected Tableau to Postgres, built multiple analysis dashboards (scatter plots, seasonal trends, correlation plots, etc.), and implemented advanced interactivity.
- **Documentation**: Updated development plan to reflect completed pipeline, analysis, and dashboard features.

## System Architecture

The system is built using Docker and consists of the following components:

- **PostgreSQL**: database for storing environmental data
- **Apache Airflow**: Workflow orchestration platform
- **Tableau**: For data visualization

## Environment Variables

- `DATA_PREFIX`: Used to resolve CSV paths in all environments. Set to `/opt/airflow` in Docker, or `.` locally.

## Troubleshooting

- If you see errors like `'Engine' object has no attribute 'cursor'`, ensure your Python dependencies match those in `airflow/requirements.txt`:
  - `pandas==1.5.3`
  - `sqlalchemy==1.4.49`
  - `psycopg2-binary==2.9.9`
- Rebuild containers after changing requirements: `docker compose build --no-cache && docker compose up -d`

## Airflow Troubleshooting

If you encounter issues such as missing tables (e.g., "relation 'connection' does not exist") or cannot log in to the Airflow UI:

1. **Check Database Connection:**
   - Ensure all Airflow services and configs point to the same Postgres database.
2. **Run Migrations:**
   - Run inside the webserver container:
     ```bash
     docker exec -it earth-monitoring-system-airflow-webserver-1 airflow db migrate
     # or
     docker exec -it earth-monitoring-system-airflow-webserver-1 airflow db upgrade
     ```
3. **Reset Metadata DB (if needed):**
   - WARNING: This will wipe all Airflow metadata (DAG runs, users, etc.).
     ```bash
     docker exec -it earth-monitoring-system-airflow-webserver-1 airflow db reset -y
     ```
4. **Recreate Admin User:**
   - After a reset, you must recreate the admin user:
     ```bash
     docker compose run airflow-webserver airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
     ```
5. **Restart Airflow Containers:**
     ```bash
     docker compose restart
     ```
6. **Orphan Containers:**
   - If you see warnings about orphan containers, clean them up with:
     ```bash
     docker compose down --remove-orphans
     ```
7. **Check Logs:**
   - Always check the Airflow webserver logs for detailed error messages.