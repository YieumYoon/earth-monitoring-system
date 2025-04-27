# Earth Monitoring System

A data pipeline for collecting, processing, and visualizing environmental data from multiple sources.

## Project Overview

The Earth Monitoring System is a comprehensive data pipeline designed to:

1. Collect environmental data from multiple sources (air quality, climate data)
2. Process and transform the data using dbt
3. Orchestrate workflows with Apache Airflow
4. Visualize the results with Tableau

## System Architecture

The system is built using Docker and consists of the following components:

- **PostgreSQL with PostGIS**: Spatial database for storing environmental data
- **Apache Airflow**: Workflow orchestration platform
- **dbt (data build tool)**: Data transformation tool
- **Python data collectors**: Scripts for fetching data from various APIs
- **Tableau**: For data visualization

## Directory Structure

```
earth-monitoring-system/
├── airflow/
│   ├── dags/             # Airflow DAG definitions
│   ├── logs/             # Airflow logs
│   └── config/           # Airflow configuration
├── data_collection/
│   ├── fetch_openaq.py   # Script to fetch air quality data
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Custom Docker image for data collection
├── dbt/
│   ├── models/
│   │   ├── staging/      # Staging models
│   │   └── mart/         # Mart models for analysis
│   ├── dbt_project.yml   # dbt project configuration
│   └── profiles.yml      # dbt connection profiles
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

### Running the Pipeline

You can run the pipeline in two ways:

1. **Manually**: Trigger the DAG from the Airflow web interface
2. **Scheduled**: The DAG is configured to run daily

## Data Sources

### Air Quality Data
- Source: OpenAQ API
- Parameters: PM2.5, PM10, O3, NO2, SO2, CO
- Coverage: Global

### Climate Data (Future Implementation)
- Source: NOAA Climate Data API
- Parameters: Temperature, precipitation, humidity
- Coverage: Global

## Development

### Adding a New Data Source

1. Create a new Python script in the `data_collection` directory
2. Update the Airflow DAG in `airflow/dags/earth_monitoring_dag.py`
3. Create new dbt models in the `dbt/models` directory

### Modifying Data Transformations

1. Edit the existing models in `dbt/models/` or add new ones
2. Run `dbt run` to test your changes

## Visualization

Connect Tableau to the PostgreSQL database:
- Host: localhost
- Port: 5432
- Database: earth_monitoring
- Username: postgres
- Password: postgres
- Schema: processed

## Maintenance

### Logs
- Airflow logs: `./airflow/logs/`
- Docker logs: `docker compose logs`

### Database Management
- Connect to PostgreSQL: `docker exec -it earth_monitoring_postgres psql -U postgres -d earth_monitoring`

## Contributors

- [Your Name]

## License

[Choose an appropriate license]