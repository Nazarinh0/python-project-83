### Hexlet tests, linter status and other:
[![Actions Status](https://github.com/Nazarinh0/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/Nazarinh0/python-project-83/actions)
[![Linter check](https://github.com/Nazarinh0/python-project-83/workflows/linter-check/badge.svg)](https://github.com/Nazarinh0/python-project-83/actions/workflows/linter-check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/c8c380438c971d5e4efd/maintainability)](https://codeclimate.com/github/Nazarinh0/python-project-83/maintainability)

## PAGE ANALYZER
This is a web application built using Python on the Flask framework. 
It allows users to add websites and perform basic "SEO checks" on them.

**Technical Stack:**
- Python version 3.11
- Flask version 2.2.2
- PostgreSQL version 14.5
- Bootstrap version 5.2.3

**Dependencies:**
- [Flask](https://github.com/pallets/flask/)
- [gunicorn](https://github.com/benoitc/gunicorn)
- [psycopg2](https://github.com/psycopg/psycopg2)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [validators](https://github.com/python-validators/validators)
- [requests](https://github.com/psf/requests)
- [beautifulsoup](https://code.launchpad.net/beautifulsoup)

### How it works
On this app, you can add sites to the main page by entering a URL, 
perform "SEO checks" to receive basic information about it. 
Users can add as many websites and checks as they want.

### Installation
1. Clone the project
2. Create a PostgreSQL database using the provided cheatsheet (database.sql)
3. Create a .env file and add the necessary variables or add them directly to your environment using the export command
4. Run `make dev` for debugging (with WSGI debug set to 'True'), or `make start` for production (using gunicorn)