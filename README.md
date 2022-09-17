# example todo applications with Flask framework

There are three example applications all using Flask.

- todos_mvc: classic mvc web stack
- todos_rest_sql: REST api stack
- todos_rest_singlefile: a miminal single-file flask REST api stack
  - raw sql data access implementation

## python environment setup

For each stack, environment is set by its own Dockerfile.

For a local development environment, use pyenv venv setup:

```sh
# create .python-version file with v3.7.2
pyenv shell 3.7.2
# venv is natively supported in python v3.4+
python -m venv venv
# activate venv:
source venv/bin/activate
# install pkgs
pip install -r requirements.txt

# to deactivate venv:
(venv) > deactivate
```

## todos_mvc app

Implementations:

- MVC stack, html templates and sqlalchemy orm
- Sementic-UI is used for page styles
- Save a web uploaded file to a BLOB db column

To run in dev mode,
first, install python environment,
then run:

```sh
cd todos_mvc
# use -m to avoid 'flask command not found' error
# -m flag enables python to recognize 3rd perty modules
export FLASK_APP=mvc
export FLASK_ENV=development
python -m flask run
```

Debug and reloader are enabled by development env.
And reloader is enabled when debug is enabled.
To enable debug in a non-dev env:

```sh
export FLASK_DEBUG=1
```

To run in terminal shell model:

```sh
python -m flask shell
```

to run in gunicorn for a production like env

```sh
pip install gunicorn
# set sync worker count to 4
gunicorn -b localhost:8000 -w 4 'mvc:create_app()'
```

build docker image:

```sh
docker build -t todosmvc-flask .
# check built image
docker images
```

run container:

```sh
docker run --name todomvc-flask -p 5000:5000 --rm todosmvc-flask
# add -d in detached mode
docker run --name todomvc-flask -d -p 5000:5000 --rm todosmvc-flask
```

container server is at http://127.0.0.1:5000/todos

## todo_rest_sql app

This todo app is REST only, no web html UI.

Also, this app uses raw sql executions for cruds.

App structure follows: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

App structure:

```
todo_rest_sql
|- __init__.py: package bootstrap
|- db.py: database config and bootstrap
|- schema.sql: DDL for db.py to initialize
|- routes.py: routes and actions
|- todos_app.py: main app entry for flask run
|- todos_rest_sql.db: sqlite3 db file
```

Run this at the project root folder level:

```sh
export FLASK_APP=todos_app.py
export FLASK_ENV=development
flask init-db
flask run
```

No need to re-run 'init-db' for successive runs unless a db reset is needed.
