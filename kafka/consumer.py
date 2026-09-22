from kafka import KafkaConsumer
import json
import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

# Snowflake connection
conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE")
)

cursor = conn.cursor()

# Kafka connection
consumer = KafkaConsumer(
    "atmosync-sensor-data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("==============================")
print(" AtmoSync Kafka → Snowflake")
print("==============================")
print("Waiting for sensor data...")
print("Press CTRL+C to stop.")
print()

try:
    for message in consumer:
        data = message.value

        if "timestamp" not in data:
            print("Old message skipped (timestamp missing).")
            print()
            continue

        print("Data received from Kafka:")
        print(data)

        cursor.execute("""
            INSERT INTO SENSOR_DATA
            (
                CONTAINER_ID,
                LOCATION,
                TEMPERATURE,
                HUMIDITY,
                RAINFALL,
                WIND_SPEED,
                RECORDED_AT
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data["container_id"],
            data["location"],
            data["temperature"],
            data["humidity"],
            data["rainfall"],
            data["wind_speed"],
            data["timestamp"]
        ))

        conn.commit()

        print("Data inserted into Snowflake! ✅")
        print()

except KeyboardInterrupt:
    print("\nConsumer stopped.")

finally:
    cursor.close()
    conn.close()
    consumer.close()
