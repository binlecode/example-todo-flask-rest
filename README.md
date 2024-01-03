# todos Flask RESTful API stack

This todo app provides REST api for todo crud service.
It uses raw sql for resource persistence in sqlite3 database, in order to 
demonstrate the low-level database initialization with flask application 
instance.

To run dev server:

```sh
FLASK_APP=rest FLASK_DEBUG=1 flask run

# run interactive shell
FLASK_APP=rest FLASK_DEBUG=1 flask shell
```

## local development

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

Run flask:

```sh
export FLASK_APP=rest
export FLASK_DEBUG=1
flask init-db
flask run
```

No need to re-run 'init-db' for successive runs unless a db reset is needed.

## project bootstrap

App structure is based on:
[flaskr tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/).

Project dependencies:

```sh
pyenv shell 3.10
python -m venv venv
source venv/bin/activate
pip install -U pip
pip install flask zipp black
pip freeze > requirements.txt
```
