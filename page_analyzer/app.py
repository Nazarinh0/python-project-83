from datetime import date
from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect, url_for, \
    flash, get_flashed_messages
from dotenv import load_dotenv
import os
import page_analyzer.db as db
from validators import url as validator

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def urls_add():
    url = request.form.get('url')

    if not validator(url):
        flash('Некорректный URL', 'danger')
        return render_template(
            'index.html',
            messages=get_flashed_messages(with_categories=True)
        )

    if db.exist_url(url):
        flash('Страница уже существует', 'danger')
        return render_template(
            'index.html',
            messages=get_flashed_messages(with_categories=True)
        )
    created_at = str(date.today())

    with db.connect() as conn:
        with conn.cursor() as curr:
            curr.execute(
                """
                INSERT INTO urls (name, created_at)
                VALUES (%(name)s, %(created_at)s)
                RETURNING id;
                """,
                {'name': url, 'created_at': created_at})
            url_id = curr.fetchone()[0]

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls_show', id=url_id))


@app.route('/urls/<int:id>')
def urls_show(id):
    url = db.find_url(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'show.html',
        url=url,
        messages=messages
    )


def normalize(url):
    o = urlparse(url)
    return f'{o.scheme}://{o.netloc}'
