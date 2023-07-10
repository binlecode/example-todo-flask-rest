# todos Flask RESTful API stack

This todo app is REST only, no web UI.
Also, this app uses raw sql executions for cruds.

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

## project structure

App structure:

```
rest
|- __init__.py: package bootstrap
|- db.py: database config and bootstrap
|- schema.sql: DDL for db.py to initialize
|- routes.py: routes and actions
|- todos_app.py: main app entry for flask run
```

Project dependencies:

```sh
pyenv shell 3.10
python -m venv venv
source venv/bin/activate
pip install -U pip
pip install flask zipp
pip freeze > requirements.txt
```
