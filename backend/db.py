# backend/db.py
import psycopg2

def get_conn():
    return psycopg2.connect(
        dbname="ragdb",
        user="raguser",
        password="ragpass",
        host="localhost",
        port=5432,
    )
