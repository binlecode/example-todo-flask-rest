# __init__.py
#
# basic app structure ref:
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
#  


from flask import Flask
import os
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)


app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(basedir, 'todos_rest_sql.db'),
)


# load db utils
from todos_rest_sql import db
db.init_app(app)


# load routes at the bottom
# The bottom import is a workaround to avoid circular imports
# todo: not good, need to adopt blueprint/app_factory pattern
from todos_rest_sql import routes
