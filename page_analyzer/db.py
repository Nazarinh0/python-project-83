from dotenv import load_dotenv
import psycopg2
import os
from datetime import date

load_dotenv()


def connect():
    database = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database)
    return conn


def exist_url(url):
    with connect().cursor() as cursor:
        cursor.execute(
            """
            SELECT id FROM urls
            WHERE name = %(url)s;
            """,
            {'url': url})
        id = cursor.fetchone()
    if id:
        return True
    return False


def find_url(id):
    with connect().cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM urls
            WHERE id=%(id)s;
            """,
            {'id': id})
        row = cursor.fetchone()
    url_id, name, created_at = row
    return {
        'id': url_id,
        'name': name,
        'created_at': created_at
    }


def all_urls():
    with connect().cursor() as cursor:
        cursor.execute(
            "SELECT * FROM urls;")
        rows = cursor.fetchall()
    urls = []
    for row in rows:
        url = {'id': row[0], 'name': row[1]}
        urls.append(url)
    return urls


def add_url(url):
    created_at = str(date.today())
    with connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """
                INSERT INTO urls (name, created_at)
                VALUES (%(name)s, %(created_at)s)
                RETURNING id;
                """,
                {'name': url, 'created_at': created_at})
            url_id = curr.fetchone()[0]
    return url_id
