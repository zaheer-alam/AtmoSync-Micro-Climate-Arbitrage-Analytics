import csv
from connection import get_connection


def load_historical_commodity_prices():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS HISTORICAL_COMMODITY_PRICES (
                price_date DATE,
                commodity VARCHAR(50),
                market VARCHAR(50),
                price_per_kg FLOAT
            )
        """)

        cursor.execute("TRUNCATE TABLE HISTORICAL_COMMODITY_PRICES")

        with open("data/historical_commodity_prices.csv", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cursor.execute(
                    """
                    INSERT INTO HISTORICAL_COMMODITY_PRICES
                    (price_date, commodity, market, price_per_kg)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        row["price_date"],
                        row["commodity"],
                        row["market"],
                        float(row["price_per_kg"]),
                    ),
                )

        conn.commit()
        print("Historical commodity pricing data loaded successfully!")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    load_historical_commodity_prices()
