

## pyenv and virtualenv

```sh
pyenv virtualenv 3.7.2 p372-flask
pip install -r requirements.txt
```


## todos_mvc app 

This is an MVC stack, with html templates.

run app:

```sh
export FLASK_APP=todos_mvc
export FLASK_ENV=development
flask init-db
flask run
```



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
