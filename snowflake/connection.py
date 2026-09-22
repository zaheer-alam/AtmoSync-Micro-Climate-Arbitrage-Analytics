import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE")
)

cursor = conn.cursor()

cursor.execute("""
    INSERT INTO SENSOR_DATA
    (CONTAINER_ID, LOCATION, TEMPERATURE, HUMIDITY, RAINFALL, WIND_SPEED, RECORDED_AT)
    VALUES
    ('C001', 'Pune', 28.5, 65.0, 2.5, 12.0, CURRENT_TIMESTAMP())
""")

conn.commit()

print("Test data inserted successfully!")

cursor.close()
conn.close()
