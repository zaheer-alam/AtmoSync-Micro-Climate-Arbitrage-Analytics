import requests
from database import save_climate_data


def get_weather(city):
    # Find city coordinates
    location_url = "https://geocoding-api.open-meteo.com/v1/search"

    location_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    location_response = requests.get(
        location_url,
        params=location_params
    )

    if location_response.status_code != 200:
        print("Could not find location.")
        return

    location_data = location_response.json()

    if "results" not in location_data:
        print("City not found.")
        return

    location = location_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    # Get weather data
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,rain,wind_speed_10m"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params
    )

    if weather_response.status_code != 200:
        print("Could not fetch weather data.")
        return

    weather_data = weather_response.json()
    current = weather_data["current"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    rainfall = current["rain"]
    wind_speed = current["wind_speed_10m"]

    print("City:", location["name"])
    print("Temperature:", temperature, "°C")
    print("Humidity:", humidity, "%")
    print("Rainfall:", rainfall, "mm")
    print("Wind Speed:", wind_speed, "km/h")

    # Save weather data to database
    save_climate_data(
        location["name"],
        temperature,
        humidity,
        rainfall,
        wind_speed
    )
