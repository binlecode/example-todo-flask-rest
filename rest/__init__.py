from flask import Flask
import os
from rest import db

basedir = os.path.abspath(os.path.dirname(__file__))

# todo: adopt app factory pattern to allow for multiple instances
app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY="dev",
    DATABASE=os.path.join(basedir, "todos.db"),
)

db.init_app(app)

# load routes at the bottom
# putting this import at bottom is a workaround to avoid circular imports
# todo: adopt blueprint for more and complex routes
from rest import routes
