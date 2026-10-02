# AtmoSync – Micro-Climate Arbitrage Analytics

AtmoSync is an end-to-end data analytics project for monitoring micro-climate conditions around agricultural commodity containers, identifying potential spoilage risk, and evaluating possible market rerouting opportunities before estimated commodity degradation.

The project combines simulated IoT telemetry, Apache Kafka streaming, Snowflake warehousing, dbt transformations, Apache Superset dashboards, GitHub Actions automation, and high-risk email alerts.

---

## Architecture

```text
Python IoT Simulator
        ↓
Apache Kafka
        ↓
Snowflake
        ↓
dbt
        ↓
Apache Superset
        ↓
Risk Monitoring
        ↓
Gmail Email Alert
```

---

## Tech Stack

- Python 3.12
- Apache Kafka
- Docker & Docker Compose
- Snowflake
- dbt Core + dbt-snowflake
- Apache Superset
- Git & GitHub
- GitHub Actions
- Gmail SMTP
- uv
- SQLite

---

## Project Structure

```text
AtmoSync/
│
├── .github/
│   └── workflows/          # GitHub Actions workflows
├── alerts/                 # High-risk email alerts
├── app/                    # Analytics/application logic
├── data/                   # Sample and reference datasets
├── dbt_atmosync/           # dbt staging, marts and tests
├── kafka/                  # Kafka producer and consumers
├── models/                 # Python data models
├── simulator/              # IoT sensor simulator
├── snowflake/              # Snowflake connection and loaders
├── superset/               # Superset Docker configuration
├── utils/                  # Utility modules
│
├── .env.example
├── .gitignore
├── .python-version
├── compose.yaml
├── config.py
├── database.py
├── main.py
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

---

## Core Features

### 1. IoT Sensor Simulation

The simulator generates mock telemetry for agricultural commodity containers.

Each sensor event contains:

- Container ID
- Location
- Temperature
- Humidity
- Rainfall
- Wind speed
- Vibration
- Timestamp

Run the simulator:

```bash
uv run --locked python simulator/sensor_simulator.py
```

---

### 2. Apache Kafka Streaming

Apache Kafka provides the streaming layer for IoT telemetry.

Main topic:

```text
atmosync-sensor-data
```

Start Kafka:

```bash
docker compose up -d --wait
```

Create the topic if required:

```bash
docker compose exec kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --if-not-exists \
  --topic atmosync-sensor-data \
  --partitions 1 \
  --replication-factor 1
```

Run the producer:

```bash
uv run --locked python kafka/producer.py
```

Run the Snowflake consumer in another terminal:

```bash
uv run --locked python kafka/consumer.py
```

The consumer transfers Kafka telemetry into Snowflake.

---

## Snowflake Data Warehouse

Snowflake acts as the central analytics warehouse.

The project processes data for:

- Sensor telemetry
- Commodity prices
- Historical commodity prices
- Market routes
- City weather summaries
- Spoilage risk
- Spoilage arbitrage

The primary telemetry table is:

```text
ATMOSYNC.RAW.SENSOR_DATA
```

Test the Snowflake connection:

```bash
uv run --locked python snowflake/test_connection.py
```

Credentials are loaded from environment variables and must not be committed to Git.

---

## dbt Analytics

dbt transforms raw Snowflake data into analytics-ready staging and mart models.

Install dbt dependencies:

```bash
uv sync --locked --extra dbt
```

Run the complete dbt pipeline:

```bash
uv run --locked --extra dbt dbt build --project-dir dbt_atmosync
```

### Staging Layer

Staging models clean and standardize:

- Sensor data
- Commodity prices
- Historical commodity prices
- Market routes

Staging models are materialized as Snowflake views.

### Analytics Marts

Important mart models include:

#### `city_weather_summary`

Provides city-level micro-climate analytics.

#### `commodity_price_trends`

Analyses historical commodity price movements across markets.

#### `spoilage_risk`

Calculates a demonstration spoilage-risk score using:

- Temperature
- Humidity
- Vibration

Risk classification:

```text
HIGH    → Risk Score >= 70
MEDIUM  → Risk Score >= 40
LOW     → Risk Score < 40
```

#### `spoilage_arbitrage`

Combines spoilage risk with market and route information to evaluate potential rerouting opportunities.

The model considers:

- Current location
- Risk score and risk level
- Estimated hours to spoil
- Commodity prices
- Route distance
- Estimated travel time
- Arbitrage gain per kg
- Safety margin

Analytics marts are materialized as Snowflake tables for repeated BI queries.

---

## Spoilage Arbitrage Use Case

The primary analytical workflow is:

```text
Container Telemetry
        ↓
Spoilage Risk
        ↓
Estimated Spoilage Time
        ↓
Market Prices + Route Distance
        ↓
Travel-Time Feasibility
        ↓
Potential Rerouting Opportunity
```

For example, when environmental conditions increase estimated spoilage risk, AtmoSync can evaluate whether another market is reachable within the estimated safe time and whether that route provides a potential price advantage.

The current risk scoring, commodity prices, route distances, spoilage-time estimates, and transport-speed assumptions are demonstration values for this academic project. They are not scientifically validated spoilage predictions or guaranteed trading profits.

---

## Apache Superset Dashboards

Start Superset:

```bash
docker compose --env-file .env -f superset/compose.yaml up -d
```

Open:

```text
http://localhost:8088
```

Two dashboards are included in the project.

### AtmoSync Micro-Climate Analytics

Published dashboard for environmental telemetry monitoring.

Visualizations include:

- Average Temperature by City
- Average Humidity by City
- Average Rainfall by City
- Average Wind Speed by City
- Total Readings by City

### AtmoSync Spoilage Arbitrage Dashboard

Published dashboard for supply-chain risk and rerouting analytics.

Visualizations include:

- At-Risk Containers & Reroute Recommendations
- Arbitrage Gain by Container
- Risk Level Distribution
- Time to Spoil vs Travel Time
- Historical Commodity Price Trends

---

## High-Risk Email Alerts

AtmoSync includes Gmail SMTP-based alerts for HIGH-risk containers.

Run the alert:

```bash
uv run --locked python alerts/high_risk_alert.py
```

The script queries the Snowflake `SPOILAGE_RISK` model and sends an email when HIGH-risk containers are detected.

Required environment variables:

```text
ALERT_EMAIL_SENDER
ALERT_EMAIL_PASSWORD
ALERT_EMAIL_RECEIVER
```

For Gmail, use an App Password rather than the normal Google account password.

Never commit email credentials to Git.

---

## GitHub Actions Automation

The project includes an automated dbt workflow:

```text
.github/workflows/dbt.yml
```

The workflow:

1. Checks out the repository
2. Installs uv
3. Installs Python 3.12
4. Installs project and dbt dependencies
5. Connects to Snowflake using GitHub Repository Secrets
6. Runs the dbt build and data-quality tests

The scheduled build runs daily at:

```text
01:30 UTC
07:00 IST
```

The workflow can also be triggered manually from GitHub Actions.

---

## Data Quality

dbt tests validate important analytics fields across staging and mart models.

The project validates fields such as:

- Container ID
- Location
- Temperature
- Risk score
- Risk level
- Recommended market

Some legacy telemetry generated before vibration support can contain null vibration values. The project does not fabricate historical vibration measurements for those records.

---

## Local Weather CLI

AtmoSync also contains a menu-driven local weather application.

Run:

```bash
uv run --locked python main.py
```

Features include:

1. Get weather
2. View saved climate data
3. Calculate average temperature
4. Exit

Weather observations are stored in a local SQLite database.

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/zaheer-alam/AtmoSync-Micro-Climate-Arbitrage-Analytics.git
cd AtmoSync-Micro-Climate-Arbitrage-Analytics
```

### 2. Install Dependencies

Install uv first, then run:

```bash
uv sync --locked
```

For dbt:

```bash
uv sync --locked --extra dbt
```

### 3. Configure Environment Variables

Use `.env.example` as the configuration reference.

Create a local `.env` file containing the required Kafka, Snowflake, Superset, and email-alert settings.

Never commit the real `.env` file.

### 4. Start Kafka

```bash
docker compose up -d --wait
```

### 5. Run the Producer

```bash
uv run --locked python kafka/producer.py
```

### 6. Run the Consumer

In another terminal:

```bash
uv run --locked python kafka/consumer.py
```

### 7. Run dbt

```bash
uv run --locked --extra dbt dbt build --project-dir dbt_atmosync
```

### 8. Start Superset

```bash
docker compose --env-file .env -f superset/compose.yaml up -d
```

### 9. Run the Alert Check

```bash
uv run --locked python alerts/high_risk_alert.py
```

---

## Security

Never commit:

```text
.env
.venv/
Passwords
Snowflake credentials
Gmail App Passwords
API keys
Superset secret keys
```

Secrets should be stored in local environment variables or GitHub Repository Secrets.

---

## Current Limitations

AtmoSync is an academic data-analytics demonstration project.

Current limitations include:

- IoT telemetry is simulated.
- Commodity prices are mock/sample data.
- Historical prices are sample data.
- Market route distances are demonstration data.
- Spoilage-risk scoring is a heuristic.
- Transport-time calculations use simplified assumptions.
- Kafka ingestion is not a production-grade exactly-once pipeline.
- Superset is configured for local development.
- Email notification uses a basic SMTP workflow.

---

## Future Improvements

Possible future improvements include:

- Real IoT sensor integration
- Live commodity-price APIs
- Real route and traffic data
- Commodity-specific degradation models
- Machine-learning-based spoilage prediction
- Durable Kafka consumer-group and offset management
- Stronger ingestion deduplication
- Production Snowflake access controls
- Production Superset deployment
- Advanced alerting and monitoring
- Support for additional commodities and markets

---

## Project Goal

AtmoSync demonstrates an end-to-end modern data analytics pipeline:

```text
IoT Telemetry
      ↓
Apache Kafka
      ↓
Snowflake
      ↓
dbt
      ↓
Apache Superset
      ↓
Risk Monitoring & Email Alerts
```

The final system demonstrates how streaming telemetry and analytics can be used to monitor micro-climate conditions, identify containers requiring attention, analyse commodity price trends, and evaluate potential rerouting opportunities before estimated commodity degradation.
