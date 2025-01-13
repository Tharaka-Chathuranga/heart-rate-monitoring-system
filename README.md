
# Heart Rate Monitoring System

## Overview

The Heart Rate Monitoring System is an event-driven microservices architecture designed to monitor and analyze heart rate data in real-time and over historical periods. The system consists of several microservices that work together to provide accurate and timely alerts for potential heart-related issues.

## Microservices

### 1. Data Ingestion Service
- **Description**: Continuously ingests heart rate data from the app and stores it in the Time-Series Database.
- **Technology**: Python, Kafka

### 2. Real-Time Monitoring Service
- **Description**: Subscribes to the Event Queue to receive real-time heart rate data, runs anomaly detection algorithms, and triggers alerts if risky patterns are detected.
- **Technology**: Python, Kafka, Pandas, Numpy

### 3. Historical Data Analysis Service
- **Description**: Performs trend analysis on a scheduled basis to establish a personalized baseline for each user.
- **Technology**: Python, Pandas, SQLAlchemy, PostgreSQL

### 4. Alert Service
- **Description**: Sends notifications to users or healthcare providers when anomalies are detected.
- **Technology**: Python

### 5. API Gateway
- **Description**: Routes and secures API requests to the appropriate microservices.
- **Technology**: Node.js

## Folder Structure

```plaintext
heart-rate-monitoring-system/
├── services/
│   ├── data-ingestion/
│   ├── real-time-monitoring/
│   │   └── src/
│   │       ├── anomaly_detection/
│   │       │   └── detector.py
│   │       ├── alert_service/
│   │       │   └── trigger.py
│   │       └── main.py
│   ├── historical-analysis/
│   │   └── src/
│   │       ├── analysis.py
│   │       └── main.py
│   ├── alert-service/
│   └── api-gateway/
├── event-queue/
│   ├── docker-compose.yml
│   └── kafka-config/
├── database/
│   ├── time-series-db/
│   └── user-profile-db/
├── shared/
│   ├── models/
│   ├── utils/
│   └── config/
└── deployment/
    ├── k8s/
    └── terraform/
```

## Getting Started

### Prerequisites
- Docker
- Python 3.8+
- PostgreSQL
- Kafka

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Tharaka-Chathuranga/heart-rate-monitoring-system.git
    cd heart-rate-monitoring-system
    ```

2. **Set up Kafka**:
    ```bash
    cd event-queue
    docker-compose up -d
    ```

3. **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up databases**:
    - Configure and start the Time-Series Database and User Profile Database.

### Running the Services

1. **Real-Time Monitoring Service**:
    ```bash
    cd services/real-time-monitoring/src
    python main.py
    ```

2. **Historical Data Analysis Service**:
    ```bash
    cd services/historical-analysis/src
    python main.py
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

```