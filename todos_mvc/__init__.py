# __init__.py
#
# The __init__.py serves double duty:
# - it will contain the application factory,
# - and it tells Python that the flaskr directory should be treated as a package.
#
# this todos app is following app factory/blueprint pattern
#

import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config['SECRET_KEY'] = 'todo-dev-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./todos.db'
    # Flask-SQLAlchemy has its own event notification system that gets layered on top of SQLAlchemy.
    # To do this, it tracks modifications to the SQLAlchemy session. This takes extra resources, so
    # the option SQLALCHEMY_TRACK_MODIFICATIONS enables/disables the modification tracking system.
    # Suggest disabling it if not in use to save system resources.
    # To turn off the Flask-SQLAlchemy event system (and disable the warning):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # /// = relative path, //// = absolute path

    # a simple heath check page
    @app.route('/health')
    def hello():
        return 'UP'

    # setup db conn
    from todos_mvc.model import db
    db.init_app(app)

    # initialize db
    with app.app_context():
        db.create_all()

    # from todos_mvc import model

    from . import todos
    app.register_blueprint(todos.bp)

    # app.add_url_rule('/', endpoint='index')

    return app
