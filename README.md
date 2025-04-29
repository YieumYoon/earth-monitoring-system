# Earth(Seoul) Monitoring System

A data pipeline for collecting, processing, and visualizing environmental data from multiple sources.

## Progress & Milestones

### Completed
- **Environment setup**: Docker Compose with Airflow, Postgres, and volume mounts for local and containerized development.
- **Python requirements**: Version-pinned to ensure pandas, sqlalchemy, and psycopg2-binary compatibility (see `airflow/requirements.txt`).
- **Airflow connection**: Configured via Airflow UI and `docker-compose.yml` with `DATA_PREFIX` for robust CSV path resolution.
- **Data ingestion**: Python scripts and Airflow DAGs load and clean Kaggle CSV data into Postgres staging tables using pandas and SQLAlchemy.
- **Testing**: Ingestion scripts tested both locally and in Dockerized Airflow, verified with manual queries and Airflow logs.

### Next Steps
- **SQL transformation**: Write and test `transform_seoul_data.sql` to create a clean, analysis-ready table.
- **Airflow transformation task**: Add a PostgresOperator step to automate SQL transformation in the DAG.
- **Visualization**: Connect Tableau to Postgres and build analysis dashboards.
- **Documentation**: Update development plan and report progress, challenges, and solutions.

## Project Overview

The Earth(Seoul) Monitoring System is a comprehensive data pipeline designed to:

1. Collect environmental data from multiple sources (air quality, climate data)
2. Process and transform the data
3. Orchestrate workflows with Apache Airflow
4. Visualize the results with Tableau

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
├── docker-compose.yml    # Docker Compose configuration
├── README.md
└── development_plan.md
```

## Data Sources

- [Air Pollution in Seoul (Kaggle)](https://www.kaggle.com/datasets/bappekim/air-pollution-in-seoul)
- [Seoul Historical Weather Data 2024 (Kaggle)](https://www.kaggle.com/datasets/alfredkondoro/seoul-historical-weather-data-2024)

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
4. **Run ingestion DAG:**
   - Trigger manually from the Airflow UI.
   - Monitor logs for task success.
5. **Connect Tableau or psql to Postgres:**
   - Host: localhost
   - Port: 5432
   - Database: earth_monitoring
   - Username: postgres
   - Password: postgres

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Tableau Desktop (for visualization)

## Maintenance

### Database Management
- Connect to PostgreSQL: `docker exec -it earth_monitoring_postgres psql -U postgres -d earth_monitoring`

## License
MIT