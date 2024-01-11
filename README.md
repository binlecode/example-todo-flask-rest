# todos Flask RESTful API stack

This flask app includes:

- REST api for todo crud service
- raw sql for resource persistence, to show low-level database initialization
- uses sqlite3 database, but can be swapped out for other relational databases

## local development server

For a local development environment, use pyenv venv setup:

```sh
# create .python-version file with v3.10
pyenv shell 3.10
# venv is natively supported in python v3.4+
python -m venv venv
# activate venv:
source venv/bin/activate
# install pkgs
pip install -r requirements.txt
```

Run local flask development server:

```sh
export FLASK_APP=rest
export FLASK_DEBUG=1
flask init-db
flask run
```

No need to re-run 'init-db' for successive runs unless a db reset is needed.

Run local flask shell:

```sh
FLASK_APP=rest FLASK_DEBUG=1 flask shell
```

Run local gunicorn wsgi server:

```sh
SCRIPT_NAME=/todo-flask-rest \
gunicorn --bind :8000 -w 2 -t 2 --log-level=debug --access-logfile - --error-logfile - rest:app
```

## project bootstrap

App structure is based on:
[flaskr tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/).

Project dependencies:

```sh
pyenv shell 3.10
python -m venv venv
source venv/bin/activate
pip install -U pip
pip install flask zipp black gunicorn
pip freeze > requirements.txt
```
