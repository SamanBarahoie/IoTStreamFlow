
# 🚀 IoTStreamFlow: Real-Time IoT Sensor Monitoring Pipeline

**IoTStreamFlow** is a scalable, production-ready data pipeline built for real-time monitoring of IoT sensor data — specifically **temperature** and **humidity**. It integrates modern data engineering technologies for seamless **streaming**, **processing**, **storage**, **serving**, and **visualization** of sensor metrics.

---

## 🔧 Tech Stack

- **Apache Kafka** – Ingests real-time sensor data.
- **Apache Airflow** – Orchestrates batch processing (average calculations).
- **MongoDB** – Stores aggregated metrics for querying.
- **Flask API** – Serves processed data as JSON.
- **Grafana (with Infinity Plugin)** – Visualizes trends in real time.
- **Docker Compose** – Orchestrates and containerizes all services.
- **Custom Docker Network (`iot-network`)** – Enables inter-service communication.

---

## 📈 Architecture Overview

```
Kafka → Airflow → MongoDB → Flask API → Grafana
```

Each component is modular, containerized, and designed for horizontal scaling and observability.

---

## 🧩 Key Challenges & Solutions

| Challenge | Solution |
|----------|----------|
| **Grafana lacked MongoDB support** | Developed a Flask API to expose MongoDB data as JSON, connected via Infinity plugin. |
| **`NoBrokersAvailable` Kafka error in Docker** | Configured producer to use `kafka:9092` within Docker's internal network. |
| **Static average temperature values** | Introduced randomized temperature range (15–35°C) in `kafka_producer.py`. |
| **Grafana missing time field error** | Ensured timestamp field is in ISO8601 format for correct temporal mapping. |
| **Extending pipeline for humidity** | Updated DAG, API, and Grafana dashboard to support and display humidity data. |

---

## ⚙️ Prerequisites

- Docker Desktop + Docker Compose
- Python 3.9+ (optional, for local testing)
- Git

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/IoTStreamFlow.git
cd IoTStreamFlow
```

### 2. Build & Start All Services

```bash
docker-compose up --build -d
```

### 3. Access the Services

| Service | URL | Credentials |
|--------|-----|-------------|
| Airflow | http://localhost:8080 | `admin` / `admin` |
| Grafana | http://localhost:8888 | `admin` / `admin` |
| Flask API | http://localhost:5000/sensor_data | No auth |

---

## 🧪 Testing

### Generate Test Sensor Data

```bash
docker exec -it iotstreamflow-flask-api-1 python /app/kafka_producer.py
```

> Sends 100 random sensor messages (temperature: 15–35°C, humidity: 50–80%) to the `iot-sensors` Kafka topic.

### Inspect MongoDB

```bash
docker exec -it iotstreamflow-mongo-1 mongosh
use iot_db
db.sensor_data.find().pretty()
```

### Check API Output

```bash
curl http://localhost:5000/sensor_data
```

### View Dashboard

Go to [http://localhost:8888](http://localhost:8888) to view real-time visualizations of temperature and humidity.

---

## 📸 Screenshots

- 📊 **Grafana Dashboard** – Real-time, color-coded panels for temperature and humidity.
- 🌀 **Airflow DAG** – Visualized ETL orchestration.
- 📡 **API Output** – Structured JSON data served via Flask.

---

## 📽️ Demo


**click to Watch the demo**

[![Watch the demo](demo_thumb_v2.png)](https://youtu.be/cHH6ERcMTVg)

---

## 🌱 Future Improvements

- 🔔 Add Grafana alerts for critical thresholds (e.g., temp > 30°C, humidity > 75%).
- ☁️ Deploy the system on cloud (AWS/GCP/Kubernetes).
- 📉 Simulate realistic patterns (e.g., diurnal temperature changes).
- 📊 Expand pipeline with more sensors: pressure, air quality, etc.

---

## 🤝 Contributing

Contributions are welcome! Open an issue or submit a PR to help improve **IoTStreamFlow**.

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---
