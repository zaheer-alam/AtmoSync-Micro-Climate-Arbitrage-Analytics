import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

conn = snowflake.connector.connect(account=os.getenv("SNOWFLAKE_ACCOUNT"), user=os.getenv("SNOWFLAKE_USER"), password=os.getenv("SNOWFLAKE_PASSWORD"), warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"), database=os.getenv("SNOWFLAKE_DATABASE"), schema=os.getenv("SNOWFLAKE_SCHEMA"), role=os.getenv("SNOWFLAKE_ROLE"))

cur = conn.cursor()
cur.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE()")
print("Snowflake connected successfully!")
print(cur.fetchone())
cur.close()
conn.close()
