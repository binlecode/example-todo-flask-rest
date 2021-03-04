# __init__.py
#
# The __init__.py serves double duty:
# - it will contain the application factory,
# - and it tells Python that the flaskr directory should be treated as a package.
#
# this todos app is following app-factory/blueprint pattern
# app-factory prevents app from being a global variable, and also helps
# creating app for test environment
#

import os
from flask import Flask
import logging
LOG = logging.getLogger(__file__)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # secret key will be used for securely signing the session cookie
    # app.config['SECRET_KEY'] = 'todo-dev-secret'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./todos.db'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config is None:
        # load config.py, if exists
        try:
            from . import config
            app.config.from_object(config)
        except Exception as e:
            LOG.error(f'ERROR loading config: {e}')

        # load instance/config.py file
        # when instance_relative_config=True is set in Flask() call
        # slient mode to mute error if file not found in instance folder
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
    app.logger.info('sqlalchemy started database sync')
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.logger.info('sqlalchemy completed database sync')

    from . import todos
    app.register_blueprint(todos.bp)

    # app.add_url_rule('/', endpoint='index')

    return app
