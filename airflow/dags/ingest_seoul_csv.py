import os
import pandas as pd
from sqlalchemy import create_engine
from airflow.hooks.base_hook import BaseHook

# Use DATA_PREFIX env variable for flexible path resolution
DATA_PREFIX = os.environ.get("DATA_PREFIX", "/opt/airflow")

def ingest_csv_to_postgres(csv_path, table_name, schema='raw', postgres_conn_id='postgres_default', **context):
    """
    Ingest a single CSV file into a Postgres table.
    """
    # Join DATA_PREFIX with csv_path if not already absolute
    if not os.path.isabs(csv_path):
        csv_path = os.path.join(DATA_PREFIX, csv_path)
    df = pd.read_csv(csv_path)
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(' ', '_')
          .str.replace('.', '')
          .str.replace('(', '')
          .str.replace(')', '')
    )
    conn = BaseHook.get_connection(postgres_conn_id)
    engine = create_engine(f'postgresql+psycopg2://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    df.to_sql(table_name, engine, schema=schema, if_exists='replace', index=False)


def ingest_multiple_csv_to_postgres(csv_paths, table_name, schema='raw', postgres_conn_id='postgres_default', sort_column=None, filter_map=None, **context):
    """
    Ingest multiple CSV files, optionally filter by value range, concatenate, and load into a Postgres table.
    filter_map: dict mapping file path to dict with keys: column, start, end
    Example: {'file.csv': {'column': 'datetime', 'start': '2017-01-01', 'end': '2017-12-31'}}
    """
    dfs = []
    for path in csv_paths:
        # Join DATA_PREFIX with csv_path if not already absolute
        if not os.path.isabs(path):
            abs_path = os.path.join(DATA_PREFIX, path)
        else:
            abs_path = path
        df = pd.read_csv(abs_path)
        if filter_map and path in filter_map:
            f = filter_map[path]
            col = f['column']
            start = f.get('start')
            end = f.get('end')
            df[col] = pd.to_datetime(df[col])
            if start:
                df = df[df[col] >= pd.to_datetime(start)]
            if end:
                df = df[df[col] <= pd.to_datetime(end)]
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(' ', '_')
          .str.replace('.', '')
          .str.replace('(', '')
          .str.replace(')', '')
    )
    if sort_column and sort_column in df.columns:
        df = df.sort_values(sort_column)
    conn = BaseHook.get_connection(postgres_conn_id)
    engine = create_engine(f'postgresql+psycopg2://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    df.to_sql(table_name, engine, schema=schema, if_exists='replace', index=False)