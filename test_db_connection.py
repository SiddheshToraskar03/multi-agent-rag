import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        dbname="ragdb",
        user="raguser",
        password="ragpass",
        port=5432,
    )
    print("Connected to PostgreSQL from Python!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)
