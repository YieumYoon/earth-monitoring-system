from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'earth_monitoring_system',
    default_args=default_args,
    description='Fetch and process environmental data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 4, 26),
    catchup=False,
    tags=['earth', 'monitoring', 'environment'],
)

# Task 1: Start of pipeline
start = EmptyOperator(
    task_id='start_pipeline',
    dag=dag,
)

# Task 2: Fetch air quality data from OpenAQ
fetch_climate_data = BashOperator(
    task_id='fetch_climate_data',
    bash_command='cd /opt/airflow/data_collection && python fetch_historical_openaq.py',
    dag=dag,
)

# Task 3: Placeholder for NOAA climate data
# This will be implemented in the next phase
fetch_climate_data = EmptyOperator(
    task_id='fetch_climate_data',
    dag=dag,
)

# Task 4: Run dbt to transform the data
run_dbt = BashOperator(
    task_id='run_dbt_transformations',
    bash_command='cd /opt/airflow/dbt && dbt run',
    dag=dag,
)

# Task 5: End of pipeline
end = EmptyOperator(
    task_id='end_pipeline',
    dag=dag,
)

# Define the task dependencies
start >> fetch_air_quality >> fetch_climate_data >> run_dbt >> end