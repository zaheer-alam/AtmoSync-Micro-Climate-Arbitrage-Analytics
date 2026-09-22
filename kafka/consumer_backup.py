from kafka import KafkaConsumer
import json
import os
from dotenv import load_dotenv

load_dotenv()


consumer = KafkaConsumer(
    os.getenv("KAFKA_TOPIC", "atmosync-sensor-data"),
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092").split(","),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)


print("==============================")
print("   AtmoSync Kafka Consumer")
print("==============================")
print("Waiting for sensor data...")
print("Press CTRL+C to stop.")
print()


try:
    for message in consumer:
        data = message.value

        print("Sensor Data Received")
        print("------------------------------")
        print("Container ID:", data["container_id"])
        print("Location:", data["location"])
        print("Temperature:", data["temperature"], "°C")
        print("Humidity:", data["humidity"], "%")
        print("Rainfall:", data["rainfall"], "mm")
        print("Wind Speed:", data["wind_speed"], "km/h")
        print("Timestamp:", data.get("timestamp", "Not available"))
        print()

except KeyboardInterrupt:
    print("\nConsumer stopped.")

finally:
    consumer.close()
