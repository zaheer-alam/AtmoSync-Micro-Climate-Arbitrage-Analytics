import csv

from connection import get_connection


def load_market_routes():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS MARKET_ROUTES (
                current_location VARCHAR(50),
                market VARCHAR(50),
                distance_km FLOAT
            )
        """)

        cursor.execute("TRUNCATE TABLE MARKET_ROUTES")

        with open("data/market_routes.csv", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cursor.execute(
                    """
                    INSERT INTO MARKET_ROUTES
                    (current_location, market, distance_km)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        row["current_location"],
                        row["market"],
                        float(row["distance_km"]),
                    ),
                )

        conn.commit()

        print("Market route data loaded successfully! ✅")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    load_market_routes()