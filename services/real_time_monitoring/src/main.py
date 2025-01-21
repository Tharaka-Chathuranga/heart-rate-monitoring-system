# from kafka import KafkaConsumer
# from kafka.errors import NoBrokersAvailable
# import json
# import time
# import logging
# from anomaly_detection.detector import is_anomalous
# from alert_service.trigger import trigger_alert
# from db_client import write_heart_rate_data

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def create_kafka_consumer(retries=5, delay=5):
#     """Create Kafka consumer with retries"""
#     for attempt in range(retries):
#         try:
#             logger.info(f"Attempting to connect to Kafka (attempt {attempt + 1}/{retries})")
#             consumer = KafkaConsumer(
#                 'heart_rate_data',
#                 bootstrap_servers=['localhost:9092'],
#                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
#                 auto_offset_reset='earliest',
#                 group_id='heart_rate_monitoring_group'
#             )
#             consumer.topics()  # Test connection
#             logger.info("Successfully connected to Kafka")
#             return consumer
#         except NoBrokersAvailable:
#             if attempt < retries - 1:
#                 logger.warning(f"No brokers available. Retrying in {delay} seconds...")
#                 time.sleep(delay)
#             else:
#                 raise

# def main():
#     try:
#         consumer = create_kafka_consumer()

#         for message in consumer:
#             try:
#                 heart_rate_data = message.value['heart_rate']
#                 user_id = message.value['user_id']
#                 logger.info(f"Received heart rate {heart_rate_data} for user {user_id}")

#                 write_heart_rate_data(user_id, heart_rate_data)

#                 if is_anomalous(heart_rate_data):
#                     trigger_alert(user_id, heart_rate_data)

#             except Exception as e:
#                 logger.error(f"Error processing message: {e}")
#                 continue

#     except KeyboardInterrupt:
#         logger.info("Shutting down gracefully...")
#     except Exception as e:
#         logger.error(f"Fatal error: {e}")
#     finally:
#         if 'consumer' in locals():
#             consumer.close()

# if __name__ == "__main__":
#     main()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import logging
# from db_client import write_heart_rate_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*', logger=True)
socket_app = socketio.ASGIApp(socketio_server=sio, other_asgi_app=app)

@sio.event
async def connect(sid, environ):
    logger.info(f"Gateway connected: {sid}")

@sio.event
async def disconnect(sid):
    logger.info(f"Gateway disconnected: {sid}")

@sio.event
async def heart_rate(sid, data):
    try:
        heart_rate_value = data['heart_rate']
        user_id = data.get('user_id', 'default_user')
        
        # await write_heart_rate_data(user_id, heart_rate_value)
        
        processed_data = {
            'status': 'success',
            'heart_rate': heart_rate_value,
            'user_id': user_id
        }
        
        await sio.emit('heart_rate_processed', processed_data, room=sid)
        logger.info(f"Processed heart rate: {heart_rate_value} for user: {user_id}")
        
    except Exception as e:
        logger.error(f"Error processing heart rate: {e}")
        await sio.emit('error', {'error': str(e)}, room=sid)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=5002)