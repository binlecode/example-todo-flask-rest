# todos_rest_sql: REST API stack

## python environment setup

The dependencies in requirements.txt are frozen with python 3.7.13.

```sh
pyenv shell 3.7.13
python -m venv venv
source venv/bin/activate
# install pkgs
pip install -r requirements.txt
```

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
