#!/usr/bin/env python3
"""
Fetch air quality data from OpenAQ API using the Python SDK and store it in PostgreSQL.
"""
import psycopg2
import os
import logging
from datetime import datetime, timedelta
from openaq import OpenAQ

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get API key from environment variable
API_KEY = os.environ.get('OPENAQ_API_KEY')
if not API_KEY:
    logger.warning("No API key found. Set OPENAQ_API_KEY in .env file.")

# Database connection parameters - configured for Docker
DB_PARAMS = {
    'dbname': 'earth_monitoring',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'postgres',  # This matches the service name in docker-compose
    'port': '5432',
}

def fetch_openaq_data(limit=100):
    """Fetch latest air quality data from OpenAQ using the SDK."""
    try:
        # Initialize the OpenAQ client
        client = OpenAQ(api_key=API_KEY)
        
        logger.info(f"Fetching locations from OpenAQ with limit {limit}")
        
        # Get locations with air quality data
        locations_response = client.locations.list(
            limit=limit,
            page=1
        )
        
        logger.info(f"Found {len(locations_response.results)} locations")
        
        measurements = []
        for location in locations_response.results:
            # Get the latest measurements for this location
            try:
                latest = client.locations.latest(location.id)
                
                for measurement in latest.results:
                    measurements.append({
                        'location_id': str(location.id),
                        'city': location.name,
                        'country': location.country.name if location.country else '',
                        'latitude': location.coordinates.latitude,
                        'longitude': location.coordinates.longitude,
                        'parameter': measurement.parameter.name,
                        'value': measurement.value,
                        'unit': measurement.parameter.units,
                        'timestamp': measurement.datetime.utc,
                        'source_name': 'OpenAQ SDK'
                    })
            except Exception as e:
                logger.warning(f"Error fetching latest data for location {location.id}: {e}")
                continue
        
        logger.info(f"Extracted {len(measurements)} measurements")
        return measurements
    
    except Exception as e:
        logger.error(f"Error fetching data from OpenAQ: {e}")
        return []

def insert_data_to_db(data):
    """Insert OpenAQ data into PostgreSQL."""
    try:
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                conn = psycopg2.connect(**DB_PARAMS)
                break
            except psycopg2.OperationalError as e:
                retry_count += 1
                logger.warning(f"Database connection attempt {retry_count} failed: {e}")
                if retry_count >= max_retries:
                    raise
                time.sleep(5)
        cursor = conn.cursor()
        insert_sql = """
        INSERT INTO raw.air_quality 
        (location_id, city, country, latitude, longitude, parameter, value, unit, timestamp, source_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        insert_count = 0
        skip_count = 0
        for measurement in data:
            if (measurement['value'] is None or
                measurement['latitude'] is None or
                measurement['longitude'] is None or
                measurement['timestamp'] is None):
                logger.warning(f"Skipping record due to missing required fields: {measurement}")
                skip_count += 1
                continue
            try:
                cursor.execute(insert_sql, (
                    measurement['location_id'],
                    measurement['city'],
                    measurement['country'],
                    measurement['latitude'],
                    measurement['longitude'],
                    measurement['parameter'],
                    measurement['value'],
                    measurement['unit'],
                    measurement['timestamp'],
                    measurement['source_name']
                ))
                insert_count += 1
            except Exception as e:
                logger.error(f"Failed to insert record: {measurement}, error: {e}")
                conn.rollback()  # Roll back this statement, not the whole batch
        conn.commit()
        logger.info(f"Successfully inserted {insert_count} records into the database. Skipped {skip_count} records.")
    except (Exception, psycopg2.Error) as e:
        logger.error(f"Database error: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

def main():
    """Main function to fetch and store OpenAQ data."""
    logger.info("Starting data collection from OpenAQ")
    data = fetch_openaq_data(limit=500)  # Fetch up to 500 locations
    if data:
        insert_data_to_db(data)
    else:
        logger.warning("No data received from API")
    logger.info("Data collection completed")

if __name__ == "__main__":
    import time  # For retry logic
    main()