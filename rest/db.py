import sqlite3

import click
from flask import current_app
from flask.cli import with_appcontext

# db module follows this guide:
# https://flask.palletsprojects.com/en/2.0.x/tutorial/database/

# g is simple namespace object that used to store data that can access
# application level data during a request.
# g can be used as request scope storage, it is reset for each request
# g has same lifetime as application context.
from flask import g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        # return rows that behave like dicts (instead of tuples)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(event=None):
    """close db by call or event"""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def load_db():
    db = get_db()
    with current_app.open_resource("fixture.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    click.echo("Initializing application database.")
    init_db()
    click.echo("Initialized application database.")


@click.command("load-db")
@with_appcontext
def load_db_command():
    click.echo("Loading application data.")
    load_db()
    click.echo("Loaded application data.")


# define an init_app function to register functions with the given appliction
# instance
def init_app(app):
    # register close_db function with the application instance
    # close_db function is called after returning the response
    app.teardown_appcontext(close_db)
    # register command function that can be called with flask command
    app.cli.add_command(init_db_command)
    app.cli.add_command(load_db_command)
