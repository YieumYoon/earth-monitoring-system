# Earth(Seoul) Monitoring System

A data pipeline for collecting, processing, and visualizing environmental data from multiple sources.

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
└── docker-compose.yml    # Docker Compose configuration
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Tableau Desktop (for visualization)

## Environment Setup

This project requires an OpenAQ API key to fetch air quality data. 

1. Register for an API key at [OpenAQ Explorer](https://explore.openaq.org/)
2. Copy the `.env.example` file to `.env` in the data_collection directory:

### Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd earth-monitoring-system
   ```

2. Start the Docker containers:
   ```bash
   docker compose up -d
   ```

3. Initialize Airflow (first time only):
   ```bash
   docker compose run airflow-webserver airflow db init
   docker compose run airflow-webserver airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
   ```

4. Access the Airflow web interface at http://localhost:8080 and log in with username `admin` and password `admin`.


## Data Sources



https://www.kaggle.com/datasets/bappekim/air-pollution-in-seoul
https://www.kaggle.com/datasets/alfredkondoro/seoul-historical-weather-data-2024


## Visualization

Connect Tableau to the PostgreSQL database:
- Host: localhost
- Port: 5432
- Database: seoul_monitoring
- Username: postgres
- Password: postgres
- Schema: processed

## Maintenance

### Database Management
- Connect to PostgreSQL: `docker exec -it seoul_monitoring_postgres psql -U postgres -d seoul_monitoring`