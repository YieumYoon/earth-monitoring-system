import pandas as pd
from sqlalchemy import create_engine


# Air Quality Transformation (from transform_seoul_air_quality_data.sql)
def transform_air_quality(**context):
    engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres:5432/earth_monitoring')
    df = pd.read_sql('SELECT * FROM raw.seoul_air_quality_2017_2019', engine)
    df['date'] = pd.to_datetime(df['measurement_date']).dt.date
    result = df.groupby('date').agg({
        'pm10': lambda x: round(x.mean()),
        'pm25': lambda x: round(x.mean()),
        'o3': lambda x: round(x.mean(), 3),
        'no2': lambda x: round(x.mean(), 3),
        'co': lambda x: round(x.mean(), 1),
        'so2': lambda x: round(x.mean(), 3),
    }).reset_index()
    result.rename(columns={
        'pm10': 'avg_pm10',
        'pm25': 'avg_pm25',
        'o3': 'avg_o3',
        'no2': 'avg_no2',
        'co': 'avg_co',
        'so2': 'avg_so2',
    }, inplace=True)
    # Save to processed.daily_seoul_air_quality
    result.to_sql('daily_seoul_air_quality', engine, schema='processed', if_exists='replace', index=False)
    # Add unique constraint on date
    with engine.connect() as conn:
        conn.execute('''ALTER TABLE processed.daily_seoul_air_quality DROP CONSTRAINT IF EXISTS uq_daily_aq_date''')
        conn.execute('''ALTER TABLE processed.daily_seoul_air_quality ADD CONSTRAINT uq_daily_aq_date UNIQUE (date)''')

# Weather Transformation (from transform_seoul_weather_data.sql)
def transform_weather(**context):
    engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres:5432/earth_monitoring')
    query = '''
    SELECT DATE(datetime) AS date, tempmax, tempmin, temp, feelslikemax, feelslikemin, feelslike, dew, humidity, precip, precipprob, precipcover, preciptype, snow, snowdepth, windgust, windspeed, winddir, sealevelpressure, cloudcover, visibility, solarradiation, solarenergy, uvindex, severerisk, sunrise, sunset, moonphase, conditions, description, icon
    FROM raw.seoul_weather_2017_2019
    ORDER BY DATE(datetime)
'''
    df = pd.read_sql(query, engine)
    df.to_sql('daily_seoul_weather', engine, schema='processed', if_exists='replace', index=False)
    with engine.connect() as conn:
        conn.execute('''ALTER TABLE processed.daily_seoul_weather DROP CONSTRAINT IF EXISTS uq_daily_weather_date''')
        conn.execute('''ALTER TABLE processed.daily_seoul_weather ADD CONSTRAINT uq_daily_weather_date UNIQUE (date)''')

# Final Join (from transform_seoul_final_joined_table.sql)
def transform_final_joined(**context):
    engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres:5432/earth_monitoring')
    query = '''
    CREATE SCHEMA IF NOT EXISTS processed;
    DROP TABLE IF EXISTS processed.daily_seoul_air_quality_weather;
    CREATE TABLE processed.daily_seoul_air_quality_weather AS
    SELECT
        w.date,
        aq.avg_pm10,
        aq.avg_pm25,
        aq.avg_o3,
        aq.avg_no2,
        aq.avg_co,
        aq.avg_so2,
        w.tempmax,
        w.tempmin,
        w.temp,
        w.humidity,
        w.precip,
        w.precipprob,
        w.precipcover,
        w.snow,
        w.snowdepth,
        w.windgust,
        w.windspeed,
        w.winddir,
        w.sealevelpressure,
        w.cloudcover,
        w.visibility,
        w.solarradiation,
        w.solarenergy,
        w.uvindex,
        w.severerisk,
        w.sunrise,
        w.sunset,
        w.conditions,
        w.description,
        w.icon
    FROM processed.daily_seoul_weather w
    LEFT JOIN processed.daily_seoul_air_quality aq
        ON w.date = aq.date
    ORDER BY w.date;
    '''
    with engine.connect() as conn:
        for stmt in query.strip().split(';'):
            if stmt.strip():
                conn.execute(stmt)