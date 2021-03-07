import sqlite3

import click
# g is simple namespace object that used to store
# data that can access application level
# data during a request.
# g can be used as as request scope storage and is reset for each request
# g has same lifetime as application context
# current_app is a proxy to application context
# 
from flask import current_app, g
from flask.cli import cli, with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # return rows that behave like dicts (instead of tuples)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(event=None):
    """close db by call or event"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


# register functions with the appliction instance given as argument
def init_app(app):
    # close_db function is called after returning the response
    app.teardown_appcontext(close_db)
    # adds command function that can be called with flask command
    app.cli.add_command(init_db_command)

