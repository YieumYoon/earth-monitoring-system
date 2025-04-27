#!/usr/bin/env python3
"""
Fetch air quality data from OpenAQ with geographic filtering and merge with climate data.
"""
import psycopg2
import os
import logging
import time
from datetime import datetime, timedelta
from openaq import OpenAQ

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get API key from environment variable
API_KEY = os.environ.get('OPENAQ_API_KEY')
if not API_KEY:
    logger.warning("No API key found. Set OPENAQ_API_KEY in .env file.")

# Database connection parameters
DB_PARAMS = {
    'dbname': 'earth_monitoring',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'postgres',
    'port': '5432',
}

def fetch_geo_filtered_data(bbox=None, radius=None, coordinates=None, limit=100):
    """Fetch air quality data with geographic filtering."""
    try:
        # Initialize the OpenAQ client
        client = OpenAQ(api_key=API_KEY)
        
        logger.info(f"Fetching locations with geographic filtering")
        
        # Use either bbox or radius+coordinates for geographical filtering
        locations_response = client.locations.list(
            limit=limit,
            page=1,
            bbox=bbox,
            radius=radius,
            coordinates=coordinates
        )
        
        logger.info(f"Found {len(locations_response.results)} locations")
        
        # Extract location data (for later joining with climate data)
        locations = []
        for location in locations_response.results:
            locations.append({
                'id': location.id,
                'name': location.name,
                'latitude': location.coordinates.latitude,
                'longitude': location.coordinates.longitude,
                'country': location.country.name if location.country else '',
                'parameters': [p.name for p in location.parameters] if hasattr(location, 'parameters') else []
            })
            
        return locations
    
    except Exception as e:
        logger.error(f"Error fetching data from OpenAQ: {e}")
        return []

def fetch_historical_data(location_id, days_back=7):
    """Fetch historical air quality data for a location."""
    try:
        client = OpenAQ(api_key=API_KEY)
        
        # Get sensors for this location
        sensors_response = client.locations.sensors(location_id)
        
        all_measurements = []
        for sensor in sensors_response.results:
            try:
                # Calculate date range (last week)
                end_date = datetime.now().isoformat()
                start_date = (datetime.now() - timedelta(days=days_back)).isoformat()
                
                # Get hourly data for this sensor
                measurements = client.measurements.list(
                    sensors_id=sensor.id,
                    date_from=start_date,
                    date_to=end_date,
                    data="hours",
                    rollup="hourly",
                    limit=500
                )
                
                logger.info(f"Found {len(measurements.results)} measurements for sensor {sensor.id}")
                
                for m in measurements.results:
                    all_measurements.append({
                        'location_id': location_id,
                        'sensor_id': sensor.id,
                        'parameter': sensor.parameter.name,
                        'value': m.value,
                        'timestamp': m.period.datetime_from.utc,
                        'unit': sensor.parameter.units
                    })
            except Exception as e:
                logger.warning(f"Error fetching data for sensor {sensor.id}: {e}")
                continue
                
        return all_measurements
    
    except Exception as e:
        logger.error(f"Error fetching historical data: {e}")
        return []

def store_historical_data(data):
    """Store historical data in PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.air_quality_hourly (
            id SERIAL PRIMARY KEY,
            location_id TEXT,
            sensor_id TEXT,
            parameter TEXT,
            value FLOAT,
            unit TEXT,
            timestamp TIMESTAMP,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Insert data
        insert_sql = """
        INSERT INTO raw.air_quality_hourly 
        (location_id, sensor_id, parameter, value, unit, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # Process each measurement
        insert_count = 0
        for m in data:
            # Skip entries without a value
            if m['value'] is None:
                continue
                
            cursor.execute(insert_sql, (
                m['location_id'],
                m['sensor_id'],
                m['parameter'],
                m['value'],
                m['unit'],
                m['timestamp']
            ))
            insert_count += 1
        
        conn.commit()
        logger.info(f"Successfully inserted {insert_count} historical records into the database")
    
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
    logger.info("Starting historical data collection from OpenAQ")
    
    # US West Coast bbox (min_lon, min_lat, max_lon, max_lat)
    west_coast_bbox = (-124.7844079, 32.5343198, -114.1315346, 49.0024442)
    
    # Fetch locations in this region
    locations = fetch_geo_filtered_data(bbox=west_coast_bbox, limit=20)
    
    # Fetch historical data for each location
    for location in locations:
        logger.info(f"Fetching data for location: {location['name']}")
        historical_data = fetch_historical_data(location['id'], days_back=3)
        if historical_data:
            store_historical_data(historical_data)
        time.sleep(1)  # Avoid rate limits
    
    logger.info("Historical data collection completed")

if __name__ == "__main__":
    main()