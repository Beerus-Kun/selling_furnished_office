import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conn():

    conn = psycopg2.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD")
    )
    conn.autocommit = True
    return conn

