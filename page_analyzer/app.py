from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
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
    raw_url = request.form.get('url')
    url = normalize(raw_url)
    if not validator(url):
        flash('Некорректный URL', 'danger')
        return render_template(
            'index.html',
            messages=get_flashed_messages(with_categories=True)
        ), 422
    id = db.exist_url(url)
    if id:
        flash('Страница уже существует', 'info')
        return redirect(url_for('urls_show', id=id))
    url_id = db.add_url(url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls_show', id=url_id))


@app.route('/urls/<int:id>')
def urls_show(id):
    url = db.find_url(id)
    checks = db.all_checks(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'show.html',
        url=url,
        messages=messages,
        checks=checks
    )


@app.route('/urls')
def urls_get():
    urls = db.all_urls()
    return render_template(
        'urls.html',
        urls=urls
    )


@app.post('/urls/<int:id>/checks')
def urls_check(id):
    url = db.find_url(id)['name']

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('urls_show', id=id))

    status_code = response.status_code
    soup = BeautifulSoup(response.text, 'lxml')
    h1 = soup.find('h1')
    h1 = h1.text if h1 else ''
    title = soup.find('title')
    title = title.text if title else ''
    description = soup.find('meta', {'name': 'description'})
    description = description['content'] if description else ''

    db.check_url(
        id,
        status_code=status_code,
        h1=h1,
        title=title,
        description=description
    )
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('urls_show', id=id))


def normalize(url):
    o = urlparse(url)
    return f'{o.scheme}://{o.netloc}'
