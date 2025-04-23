from flask import Flask, jsonify
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/sensor_data')
def get_sensor_data():
    client = MongoClient('mongo:27017')
    db = client['iot_db']
    collection = db['sensor_data']
    data = list(collection.find({}, {'_id': 0, 'timestamp': 1, 'avg_temperature': 1, 'avg_humidity': 1}))
    for item in data:
        if isinstance(item['timestamp'], str):
            try:
                parsed = datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00'))
                item['timestamp'] = parsed.isoformat() + 'Z'
            except ValueError:
                item['timestamp'] = datetime.now(pytz.UTC).isoformat() + 'Z'
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)