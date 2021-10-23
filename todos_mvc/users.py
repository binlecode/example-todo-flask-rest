from todos_mvc.model import Todo, User, db
from threading import currentThread
from flask import Blueprint
from flask import Flask
from flask import flash
from flask import render_template
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename
from base64 import b64encode
from flask import current_app
import os

import logging
LOG = logging.getLogger(__name__)


bp = Blueprint('users', __name__)


@bp.route('/users', methods=['GET'])
def index():
    rs = User.query.all()
    user_list = [user for user in rs]
    # for user in rs:
        # t = {
        #     'id': user.id,
        #     'username': user.username
        # }
        # user_list.append(t)

    return render_template('users/index.html', user_list=user_list, title='Todo App - Users')


@bp.route('/users/add', methods=['POST'])
def add():
    username = request.form.get('username')
    new_user = User(username=username)

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('users.index'))


@bp.route('/users/update/<user_id>', methods=['POST', 'PUT'])
def update(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        new_username = request.form.get('username')
        if user:
            user.username = new_username
            db.session.commit()
        current_app.logger.debug(f'>> user [{user.id}] was updated')
        flash(f'a user [{user.id}] was updated')
    except Exception as e:
        LOG.error(f'Failed to update user: {user}')
        LOG.error(e)
    return redirect('/users')


@bp.route('/todos/delete/<user_id>', methods=['POST', 'DELETE'])
def delete(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash(f'a user {user.id} was deleted')
    return redirect(url_for('users.index'))
