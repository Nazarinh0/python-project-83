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
        id = cursor.fetchone()[0]
    if id:
        return id
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


def all_urls():  # сюда добавить вывод url.status для последней проверки
    with connect().cursor() as cursor:
        cursor.execute(
            """
            SELECT
                urls.id,
                urls.name,
                MAX(url_checks.created_at) AS created_at,
                url_checks.status_code
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            GROUP BY urls.id, urls.name, url_checks.status_code;
            """)
        rows = cursor.fetchall()
    urls = []
    for row in rows:
        url = {
            'id': row[0],
            'name': row[1],
            'date': row[2],
            'status_code': row[3]
        }
        if not url['date']:
            url['date'] = ''
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


def check_url(id, status_code=None, h1=None, title=None, description=None):
    created_at = str(date.today())
    with connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """
                INSERT INTO url_checks (
                    url_id, status_code, h1, title, description, created_at)
                VALUES (
                %(url_id)s,
                %(status_code)s,
                %(h1)s,
                %(title)s,
                %(description)s,
                %(created_at)s)
                RETURNING url_id, created_at;
                """,
                {
                    'url_id': id,
                    'status_code': status_code,
                    'h1': h1,
                    'title': title,
                    'description': description,
                    'created_at': created_at
                })


def all_checks(id):
    with connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """SELECT
                id,
                status_code,
                COALESCE(h1, ''),
                COALESCE(title, ''),
                COALESCE(description, ''),
                DATE(created_at)
                 FROM url_checks
                WHERE url_id = %s
                ORDER BY id;""", (id,))
            rows = curr.fetchall()
            print(rows)
    checks = []
    for row in rows:
        print(row)
        check = {
            'id': row[0],
            'response_code': row[1],
            'h1': row[2],
            'title': row[3],
            'content': row[4],
            'created_at': row[5],
        }
        checks.append(check)
    return checks
