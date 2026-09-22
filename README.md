# AtmoSync – Micro-Climate Arbitrage Analytics
## Architecture

```text
Python IoT Simulator
        ↓
      Kafka
        ↓
    Snowflake
        ↓
       dbt
        ↓
 Apache Superset
```

## Tech Stack

- Python
- Apache Kafka
- Snowflake
- dbt
- Apache Superset
- Git & GitHub
- uv for Python environment/dependency management

## Project Structure

```text
AtmoSync/
│
├── simulator/       # IoT sensor data generator
├── kafka/           # Kafka producer/consumer
├── snowflake/       # Snowflake SQL and ingestion
├── dbt_atmosync/    # dbt transformations
├── superset/        # Dashboard-related files
├── data/            # Reference/sample data
│
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/zaheer-alam/AtmoSync-Micro-Climate-Arbitrage-Analytics.git
cd AtmoSync-Micro-Climate-Arbitrage-Analytics
```

### 2. Install uv

Make sure `uv` is installed on your system.

### 3. Set up the project environment

```bash
uv sync --locked
```

This automatically creates `.venv` and installs the required dependencies.

You do **not** need to manually create a virtual environment.

### 4. Run Python scripts

Example:

```bash
uv run python simulator/sensor_simulator.py
```

Run commands from the repository root. Python 3.12 or newer is required.
The weather CLI is available with `uv run --locked python main.py`; it writes to
the local SQLite database and needs internet access for weather lookups.

### 5. Run the local telemetry demo

Start Docker Desktop first. This single-node broker is for local development;
its port is exposed only on the local machine. Configuration follows the
[official Apache Kafka Docker setup](https://kafka.apache.org/39/getting-started/docker/).

```bash
docker compose up -d --wait
docker compose exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --if-not-exists --topic atmosync-sensor-data --partitions 1 --replication-factor 1
uv run --locked python kafka/producer.py
```

In another terminal at the repository root:

```bash
uv run --locked python kafka/consumer_backup.py
```

Expect a sensor event approximately every five seconds. This consumer prints
events without contacting Snowflake. Stop each script with Ctrl+C and stop the
broker with `docker compose down`. The named volume retains broker data.

Default broker/topic values work without an `.env` file. If customization is
needed, copy `.env.example` to `.env` only when `.env` does not already exist;
otherwise add the missing settings to your existing file. A comma-separated
`KAFKA_BOOTSTRAP_SERVERS` list and `KAFKA_TOPIC` are supported by all Kafka scripts.
If you change the topic, create that same topic with the command above.

### 6. Snowflake and dbt prerequisites

`kafka/consumer.py` inserts into an existing `SENSOR_DATA` table using the
`SNOWFLAKE_*` settings documented in `.env.example`. Table provisioning and
reliable replay/deduplication are not implemented yet. Do not treat this consumer
as production-ready: it has no configured consumer group or durable replay policy.
`snowflake/connection.py` inserts a test row when executed.

Install dbt and the Snowflake adapter with `uv sync --locked --extra dbt`.
The dbt project still contains starter examples, including a null value that
fails its `not_null` test. It needs a local credentials profile and telemetry
models before it is useful. Superset currently has no dashboard assets.

### Dependency maintenance

`pyproject.toml` is the dependency source and `uv.lock` pins resolved versions.
`requirements.txt` is a generated export for pip users, not a separate package list.
After changing dependencies, regenerate it with:

```bash
uv lock
uv export --locked --no-emit-project --format requirements-txt --output-file requirements.txt
```

The optional dbt dependencies are in the lockfile; the default requirements export
includes only runtime dependencies. Existing `venv/` environments are not used by uv.

### Delivery roadmap

Track implementation evidence as the project progresses:

1. Reproducible setup and local sensor-to-Kafka demonstration.
2. Validated telemetry schema, Snowflake table setup, and reliable ingestion.
3. dbt staging models, data-quality tests, and container-risk analytics.
4. Superset dashboards with clearly documented analytical assumptions.
5. Project documentation, report, presentation, and reproducible final demo.

Commit each completed, verified change with a descriptive message. Track authored
commits separately from the repository total; both include historical work.

## Team Workflow

Create a separate branch for your assigned component.

```bash
git checkout -b feature/your-feature
```

After making changes:

```bash
git add .
git commit -m "Describe your changes"
git push -u origin feature/your-feature
```

Then create a Pull Request to merge your branch into `main`.

### Suggested Branches

```text
feature/iot-simulator
feature/kafka-pipeline
feature/snowflake-dbt
feature/superset-dashboard
```

## Important

Do not commit:

```text
.venv/
.env
credentials
API keys
```

If new dependencies are added, commit the updated `pyproject.toml` and `uv.lock`.

Other team members should then run:

```bash
git pull
uv sync
```

## Project Goal

Build an end-to-end streaming pipeline:

**IoT Telemetry → Kafka → Snowflake → dbt → Superset**

The final dashboard should help identify **at-risk containers and potential rerouting opportunities before commodity quality degrades**.
