from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import random

def consume_from_kafka():
    consumer = KafkaConsumer(
        'iot-sensors',
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='latest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    data = []
    for message in consumer:
        data.append(message.value)
        if len(data) >= random.randint(5, 15):  # تعداد تصادفی بین 5 تا 15
            break
    return data

def process_data(ti):
    data = ti.xcom_pull(task_ids='consume_kafka')
    if not data:
        return
    temperatures = [item['temperature'] for item in data]
    humidities = [item['humidity'] for item in data]
    avg_temp = sum(temperatures) / len(temperatures)
    avg_humidity = sum(humidities) / len(humidities)
    result = {
        'timestamp': datetime.now().isoformat(),
        'avg_temperature': avg_temp,
        'avg_humidity': avg_humidity
    }
    return result

def store_in_mongo(ti):
    result = ti.xcom_pull(task_ids='process_data')
    if not result:
        return
    client = MongoClient('mongo:27017')
    db = client['iot_db']
    collection = db['sensor_data']
    collection.insert_one(result)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 22),
    'retries': 1,
}

with DAG(
    'realtime_iot_pipeline',
    default_args=default_args,
    schedule_interval='@continuous',
    catchup=False,
    max_active_runs=1
) as dag:
    consume_task = PythonOperator(
        task_id='consume_kafka',
        python_callable=consume_from_kafka,
    )
    process_task = PythonOperator(
        task_id='process_data',
        python_callable=process_data,
    )
    store_task = PythonOperator(
        task_id='store_in_mongo',
        python_callable=store_in_mongo,
    )
    consume_task >> process_task >> store_task