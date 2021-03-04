

## pyenv and virtualenv

```sh
pyenv local 3.7.2
# verify python version
which python
cd <project-root>
# venv is natively supported in python 3
python -m venv venv
# install pkgs
pip install -r requirements.txt
```


## todos_mvc app 

This is an MVC stack, with html templates.

run app:

```sh
export FLASK_APP=todos_mvc
export FLASK_ENV=development
# use -m to avoid 'flask command not found' error
# -m flag enables python recognize 3rd perty modules
python -m flask run
```

debug and reloader are enabled by development env, 
if choose not to use dev env:
```sh
export FLASK_DEBUG=1
```
by default, reloader is enabled when debug is enabled.


to run in gunicorn for a production live env
```sh
pip install gunicorn
# set worker count to 4 for a more prouction like concurrent demand
gunicorn -b localhost:8000 -w 2 'todos_mvc:create_app()'
```

build docker image:
```sh
docker build -t todosmvc-flask .
# check built image
docker images
```

run container:
```sh
docker run --name microblog -d -p 8000:5000 --rm todosmvc-flask
```
container server is at http://127.0.0.1:8000/todos





## todo_rest_sql app

This todo app is REST only, no web html UI.

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
