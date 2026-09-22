import random
import time
from datetime import datetime


locations = [
    "Pune",
    "Mumbai",
    "Nashik",
    "Delhi",
    "Bangalore"
]


def generate_sensor_data():
    container_id = f"C{random.randint(1, 10):03d}"
    location = random.choice(locations)

    temperature = round(random.uniform(20, 40), 2)
    humidity = round(random.uniform(40, 90), 2)
    rainfall = round(random.uniform(0, 10), 2)
    wind_speed = round(random.uniform(5, 25), 2)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "container_id": container_id,
        "location": location,
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
        "wind_speed": wind_speed,
        "timestamp": timestamp
    }


def main():
    print("==============================")
    print("      AtmoSync IoT Simulator")
    print("==============================")
    print()

    while True:
        data = generate_sensor_data()

        print("Sensor Data Generated")
        print("------------------------------")
        print("Container ID:", data["container_id"])
        print("Location:", data["location"])
        print("Temperature:", data["temperature"], "°C")
        print("Humidity:", data["humidity"], "%")
        print("Rainfall:", data["rainfall"], "mm")
        print("Wind Speed:", data["wind_speed"], "km/h")
        print("Timestamp:", data["timestamp"])
        print()

        time.sleep(5)


if __name__ == "__main__":
    main()
