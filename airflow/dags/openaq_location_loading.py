from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from extract_openaq_raw import extract_and_store_openaq_location

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG for infrequent location metadata loading
location_dag = DAG(
    'openaq_location_metadata_loading',
    default_args=default_args,
    description='Load and update OpenAQ station/location metadata',
    schedule_interval=timedelta(days=30),
    start_date=datetime(2025, 4, 26),
    catchup=False,
    tags=['earth', 'monitoring', 'metadata', 'location'],
)

# Task 1: Start of pipeline
start = EmptyOperator(
    task_id='start_pipeline',
    dag=location_dag,
)

# Task 2: Fetch air quality station/location metadata from OpenAQ
fetch_air_quality_metadata = PythonOperator(
    task_id='fetch_air_quality_metadata',
    python_callable=extract_and_store_openaq_location,
    dag=location_dag,
)

# Task 3: End of pipeline
end = EmptyOperator(
    task_id='end_pipeline',
    dag=location_dag,
)

# Define task dependencies
start >> fetch_air_quality_metadata >> end