class ClimateData:
    def __init__(
        self,
        city,
        temperature,
        humidity,
        rainfall,
        wind_speed,
        timestamp
    ):
        self.city = city
        self.temperature = temperature
        self.humidity = humidity
        self.rainfall = rainfall
        self.wind_speed = wind_speed
        self.timestamp = timestamp

    def display(self):
        print(f"City: {self.city}")
        print(f"Temperature: {self.temperature} °C")
        print(f"Humidity: {self.humidity}%")
        print(f"Rainfall: {self.rainfall} mm")
        print(f"Wind Speed: {self.wind_speed} km/h")
        print(f"Timestamp: {self.timestamp}")
