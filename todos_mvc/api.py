import time

from todos_mvc.model import Todo, db
from threading import currentThread
from flask import Blueprint
from flask import Flask
from flask import flash
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename
from base64 import b64encode
from flask import current_app
import os

import logging
LOG = logging.getLogger(__name__)

# get system startup time
start_time = time.time()


bp = Blueprint('api', __name__)


@bp.route('/')
def hello():
    return 'Hello, Todos App with Flask!'


@bp.route('/health')
def health_check():
    return 'System up and running for {%d} seconds' % (get_uptime())


def get_uptime():
    """
    Returns the number of seconds since the program started.
    """
    # do return startTime if you just want the process start time
    return time.time() - start_time