from influxdb import InfluxDBClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# InfluxDB configuration
INFLUXDB_HOST = 'localhost'
INFLUXDB_PORT = 8086
INFLUXDB_DATABASE = 'heart_rate_db'

# Create InfluxDB client
client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)
client.switch_database(INFLUXDB_DATABASE)

def write_heart_rate_data(user_id, heart_rate):
    """Write heart rate data to InfluxDB"""
    json_body = [
        {
            "measurement": "heart_rate",
            "tags": {
                "user_id": user_id
            },
            "fields": {
                "value": heart_rate
            }
        }
    ]
    try:
        client.write_points(json_body)
        logger.info(f"Successfully wrote heart rate data for user {user_id}")
    except Exception as e:
        logger.error(f"Error writing heart rate data to InfluxDB: {e}")
        raise