from kafka import KafkaConsumer
import json
from anomaly_detection.detector import is_anomalous
from alert_service.trigger import trigger_alert

# Kafka consumer setup
consumer = KafkaConsumer(
    'heart_rate_data',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Real-time Monitoring
for message in consumer:
    heart_rate_data = message.value['heart_rate']
    user_id = message.value['user_id']

    # Anomaly Detection (basic threshold check)
    if is_anomalous(heart_rate_data):
        print(f"Anomaly detected for user {user_id}: Heart rate {heart_rate_data}")
        trigger_alert(user_id, heart_rate_data)  # Alert service notification