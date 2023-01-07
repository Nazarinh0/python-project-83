from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()


def connect():
    database = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database)
    return conn
