from kafka import KafkaProducer
import json
import time
import sys
import os

# Allow Python to find the simulator module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator.sensor_simulator import generate_sensor_data


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


print("==============================")
print("   AtmoSync Kafka Producer")
print("==============================")
print("Sending sensor data to Kafka...")
print("Press CTRL+C to stop.")
print()


try:
    while True:
        data = generate_sensor_data()

        producer.send(
            "atmosync-sensor-data",
            value=data
        )

        producer.flush()

        print("Data sent:")
        print(data)
        print()

        time.sleep(5)

except KeyboardInterrupt:
    print("\nProducer stopped.")

finally:
    producer.close()
