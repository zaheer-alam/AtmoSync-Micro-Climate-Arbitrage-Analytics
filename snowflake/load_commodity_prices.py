import csv
from connection import get_connection


def load_commodity_prices():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS COMMODITY_PRICES (
                commodity VARCHAR(50),
                market VARCHAR(50),
                price_per_kg FLOAT,
                distance_km FLOAT
            )
        """)

        cursor.execute("TRUNCATE TABLE COMMODITY_PRICES")

        with open("data/commodity_prices.csv", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cursor.execute(
                    """
                    INSERT INTO COMMODITY_PRICES
                    (commodity, market, price_per_kg, distance_km)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        row["commodity"],
                        row["market"],
                        float(row["price_per_kg"]),
                        float(row["distance_km"]),
                    ),
                )

        print("Commodity pricing data loaded successfully! ✅")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    load_commodity_prices()