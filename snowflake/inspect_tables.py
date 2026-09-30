from connection import get_connection

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("""
        SELECT
            table_name,
            row_count,
            bytes
        FROM ATMOSYNC.information_schema.tables
        WHERE table_schema = 'RAW'
        ORDER BY table_name
    """)

    print("\n===== Snowflake RAW Tables =====")

    for table_name, row_count, size_bytes in cursor.fetchall():
        size_mb = round((size_bytes or 0) / (1024 * 1024), 4)

        print(
            f"Table: {table_name} | "
            f"Rows: {row_count} | "
            f"Size: {size_mb} MB"
        )

finally:
    cursor.close()
    conn.close()
