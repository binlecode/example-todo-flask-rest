from flask import Flask
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)


app.config.from_mapping(
    SECRET_KEY="dev",
    DATABASE=os.path.join(basedir, "todos.db"),
)


# load db utils
from rest import db

db.init_app(app)


# load routes at the bottom
# The bottom import is a workaround to avoid circular imports
# todo: not good, need to adopt blueprint/app_factory pattern
from rest import routes
