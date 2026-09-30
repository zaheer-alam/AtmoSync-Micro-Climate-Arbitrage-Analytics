from connection import get_connection


conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("""
        ALTER TABLE SENSOR_DATA
        ADD COLUMN IF NOT EXISTS VIBRATION FLOAT
    """)

    conn.commit()
    print("VIBRATION column added successfully!")

finally:
    cursor.close()
    conn.close()
