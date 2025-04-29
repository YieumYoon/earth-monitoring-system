from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ingest_seoul_csv import ingest_csv_to_postgres, ingest_multiple_csv_to_postgres
from transform_seoul_data import transform_air_quality, transform_weather, transform_final_joined


# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG first
seoul_air_quality_dag = DAG(
    'ingest_seoul_csv',
    default_args=default_args,
    start_date=datetime(2024, 4, 26),
    schedule_interval=None,
    catchup=False,
    description='Ingest Seoul CSV data into raw table',
)

# Now define tasks using the DAG object
start = EmptyOperator(
    task_id='start_pipeline',
    dag=seoul_air_quality_dag,
)

ingest_air_quality_task = PythonOperator(
    task_id='ingest_air_quality_csv_to_postgres',
    python_callable=ingest_csv_to_postgres,
    op_kwargs={
        'csv_path': 'kaggle_data_source/AirPollutionSeoul/Measurement_summary.csv',  
        'table_name': 'seoul_air_quality_2017_2019',
        'schema': 'raw',
        'postgres_conn_id': 'postgres_default',
    },
    provide_context=True,
    dag=seoul_air_quality_dag,
)

ingest_weather_task = PythonOperator(
    task_id='ingest_weather_csv_to_postgres',
    python_callable=ingest_multiple_csv_to_postgres,
    op_kwargs={
        'csv_paths': [
            'kaggle_data_source/SeoulHistoricalWeatherData/seoul 2016-01-01 to 2018-01-01.csv',
            'kaggle_data_source/SeoulHistoricalWeatherData/seoul 2018-01-01 to 2020-01-01.csv',
        ],
        'table_name': 'seoul_weather_2017_2019',
        'schema': 'raw',
        'postgres_conn_id': 'postgres_default',
        'filter_map': {
            'kaggle_data_source/SeoulHistoricalWeatherData/seoul 2016-01-01 to 2018-01-01.csv': {
                'column': 'datetime',
                'start': '2017-01-01',
                'end': '2017-12-31',
            },
            'kaggle_data_source/SeoulHistoricalWeatherData/seoul 2018-01-01 to 2020-01-01.csv': {
                'column': 'datetime',
                'start': '2018-01-01',
                'end': '2019-12-31',
            }
        },
        'sort_column': 'datetime',
    },
    provide_context=True,
    dag=seoul_air_quality_dag,
)

transform_air_quality_task = PythonOperator(
    task_id='transform_air_quality',
    python_callable=transform_air_quality,
    provide_context=True,
    dag=seoul_air_quality_dag,
)

transform_weather_task = PythonOperator(
    task_id='transform_weather',
    python_callable=transform_weather,
    provide_context=True,
    dag=seoul_air_quality_dag,
)

transform_final_joined_task = PythonOperator(
    task_id='transform_final_joined',
    python_callable=transform_final_joined,
    provide_context=True,
    dag=seoul_air_quality_dag,
)

end = EmptyOperator(
    task_id='end_pipeline',
    dag=seoul_air_quality_dag,
)

# Run both ingestion tasks in parallel after start, then run transformations sequentially (air_quality -> weather -> final_joined)
start >> [ingest_air_quality_task, ingest_weather_task]
[ingest_air_quality_task >> transform_air_quality_task]
[ingest_weather_task >> transform_weather_task]
[transform_air_quality_task, transform_weather_task] >> transform_final_joined_task >> end
