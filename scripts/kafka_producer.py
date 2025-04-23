from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for i in range(100):
    data = {
        'temperature': random.uniform(15.0, 35.0),  # دمای تصادفی بین 15 تا 35
        'humidity': random.uniform(50.0, 80.0)     # رطوبت تصادفی بین 50 تا 80
    }
    producer.send('iot-sensors', data)
    time.sleep(1)
producer.flush()