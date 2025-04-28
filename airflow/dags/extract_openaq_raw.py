import os
import json
import dotenv
from openaq import OpenAQ
from pandas import json_normalize
from airflow.hooks.postgres_hook import PostgresHook
import pandas as pd

def extract_and_store_openaq_location():
    dotenv.load_dotenv()
    API_KEY = os.environ.get('OPENAQ_API_KEY')
    client = OpenAQ(api_key=API_KEY)
    response = client.locations.list(bbox=[126.914352, 37.520752, 127.051393, 37.607372])
    # Check API rate limit headers
    if hasattr(response, 'headers'):
        headers = response.headers
        remaining = getattr(headers, 'x_ratelimit_remaining', None)
        limit = getattr(headers, 'x_ratelimit_limit', None)
        if remaining is not None and int(remaining) == 0:
            raise ValueError(f"OpenAQ API rate limit exceeded: limit={limit}, remaining={remaining}")
    data = response.dict()
    df = json_normalize(data['results'])
    if df.empty:
        raise ValueError("No data fetched from OpenAQ API! Possible API or URL issue.")
    df = df.where(pd.notnull(df), None)  # Replace NaN with None

    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    insert_sql = """
        INSERT INTO raw.air_quality (
            name, locality, timezone, is_mobile, is_monitor, instruments, sensors, bounds, distance,
            datetime_first, datetime_last, country_id, country_code, country_name,
            owner_id, owner_name, provider_id, provider_name, latitude, longitude,
            datetime_first_utc, datetime_first_local, datetime_last_utc, datetime_last_local
        ) VALUES (
            %(name)s, %(locality)s, %(timezone)s, %(is_mobile)s, %(is_monitor)s, %(instruments)s, %(sensors)s, %(bounds)s, %(distance)s,
            %(datetime_first)s, %(datetime_last)s, %(country_id)s, %(country_code)s, %(country_name)s,
            %(owner_id)s, %(owner_name)s, %(provider_id)s, %(provider_name)s, %(latitude)s, %(longitude)s,
            %(datetime_first_utc)s, %(datetime_first_local)s, %(datetime_last_utc)s, %(datetime_last_local)s
        )
    """
    columns = [
        'name', 'locality', 'timezone', 'is_mobile', 'is_monitor', 'instruments', 'sensors', 'bounds', 'distance',
        'datetime_first', 'datetime_last', 'country.id', 'country.code', 'country.name',
        'owner.id', 'owner.name', 'provider.id', 'provider.name', 'coordinates.latitude', 'coordinates.longitude',
        'datetime_first.utc', 'datetime_first.local', 'datetime_last.utc', 'datetime_last.local'
    ]
    for col in columns:
        if col not in df.columns:
            df[col] = None

    for _, row in df.iterrows():
        pg_row = {
            'name': row['name'],
            'locality': row['locality'],
            'timezone': row['timezone'],
            'is_mobile': row['is_mobile'],
            'is_monitor': row['is_monitor'],
            'instruments': json.dumps(row['instruments']),
            'sensors': json.dumps(row['sensors']),
            'bounds': json.dumps(row['bounds']),
            'distance': row['distance'],
            'datetime_first': json.dumps(row['datetime_first']),
            'datetime_last': json.dumps(row['datetime_last']),
            'country_id': row['country.id'],
            'country_code': row['country.code'],
            'country_name': row['country.name'],
            'owner_id': row['owner.id'],
            'owner_name': row['owner.name'],
            'provider_id': row['provider.id'],
            'provider_name': row['provider.name'],
            'latitude': row['coordinates.latitude'],
            'longitude': row['coordinates.longitude'],
            'datetime_first_utc': row['datetime_first.utc'],
            'datetime_first_local': row['datetime_first.local'],
            'datetime_last_utc': row['datetime_last.utc'],
            'datetime_last_local': row['datetime_last.local'],
        }
        pg_hook.run(insert_sql, parameters=pg_row)
    client.close()

if __name__ == "__main__":
    extract_and_store_openaq_location()
