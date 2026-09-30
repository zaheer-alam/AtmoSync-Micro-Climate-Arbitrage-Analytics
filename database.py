import sqlite3
from datetime import datetime


def create_database():
    connection = sqlite3.connect("data/atmosync.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS climate_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            humidity REAL,
            rainfall REAL,
            wind_speed REAL,
            timestamp TEXT
        )
    """)

    connection.commit()
    connection.close()

    print("Database created successfully!")


def save_climate_data(
    city,
    temperature,
    humidity,
    rainfall,
    wind_speed
):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = sqlite3.connect("data/atmosync.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO climate_data
        (city, temperature, humidity, rainfall, wind_speed, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        city,
        temperature,
        humidity,
        rainfall,
        wind_speed,
        timestamp
    ))

    connection.commit()
    connection.close()

    print("Climate data saved successfully!")


def get_saved_climate_data():
    connection = sqlite3.connect("data/atmosync.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM climate_data
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records
