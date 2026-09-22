import sqlite3


def calculate_average_temperature(temperatures):
    if not temperatures:
        return 0

    return sum(temperatures) / len(temperatures)


def get_average_temperature():
    connection = sqlite3.connect("data/atmosync.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT temperature FROM climate_data
    """)

    records = cursor.fetchall()

    connection.close()

    temperatures = [record[0] for record in records]

    return round(calculate_average_temperature(temperatures), 2)

