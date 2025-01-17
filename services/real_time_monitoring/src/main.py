from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import time
import logging
from anomaly_detection.detector import is_anomalous
from alert_service.trigger import trigger_alert
from db_client import write_heart_rate_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_kafka_consumer(retries=5, delay=5):
    """Create Kafka consumer with retries"""
    for attempt in range(retries):
        try:
            logger.info(f"Attempting to connect to Kafka (attempt {attempt + 1}/{retries})")
            consumer = KafkaConsumer(
                'heart_rate_data',
                bootstrap_servers=['localhost:9092'],
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                auto_offset_reset='earliest',
                group_id='heart_rate_monitoring_group'
            )
            consumer.topics()  # Test connection
            logger.info("Successfully connected to Kafka")
            return consumer
        except NoBrokersAvailable:
            if attempt < retries - 1:
                logger.warning(f"No brokers available. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise

def main():
    try:
        consumer = create_kafka_consumer()

        for message in consumer:
            try:
                heart_rate_data = message.value['heart_rate']
                user_id = message.value['user_id']
                logger.info(f"Received heart rate {heart_rate_data} for user {user_id}")

                write_heart_rate_data(user_id, heart_rate_data)

                if is_anomalous(heart_rate_data):
                    trigger_alert(user_id, heart_rate_data)

            except Exception as e:
                logger.error(f"Error processing message: {e}")
                continue

    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        if 'consumer' in locals():
            consumer.close()

if __name__ == "__main__":
    main()