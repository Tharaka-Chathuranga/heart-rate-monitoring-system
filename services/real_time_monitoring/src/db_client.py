# from influxdb_client import InfluxDBClient, Point, WritePrecision
# from datetime import datetime
# import os
# from dotenv import load_dotenv
#
# # Load environment variables from .env file
# load_dotenv()
#
# # Configuration
# INFLUXDB_URL = os.getenv("INFLUXDB_URL")
# INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
# INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
# INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")
#
# # Create InfluxDB client
# client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
# write_api = client.write_api(write_options=WritePrecision.NS)
#
# def write_heart_rate_data(user_id, heart_rate):
#     point = Point("heart_rate") \
#         .tag("user_id", user_id) \
#         .field("value", heart_rate) \
#         .time(datetime.utcnow(), WritePrecision.NS)
#     write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)


from influxdb_client import InfluxDBClient, Point, WritePrecision  # Fix import
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# InfluxDB Configuration
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")

# Initialize InfluxDB client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api()

def write_heart_rate_data(user_id, heart_rate):
    """Write heart rate data to InfluxDB"""
    point = Point("heart_rate") \
        .tag("user_id", str(user_id)) \
        .field("value", float(heart_rate)) \
        .time(datetime.utcnow())

    write_api.write(bucket=INFLUXDB_BUCKET, record=point)