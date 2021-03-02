from flask import Flask
from flask import flash
from flask import render_template
from flask import request, redirect, url_for
# from flask import redirect
# from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy

from werkzeug.utils import secure_filename
from base64 import b64encode


import uuid


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, Todos App!'


# secret key needed for session to support flash scope etc
app.config['SECRET_KEY'] = 'todo-dev-secret'

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./todos.db'
# Flask-SQLAlchemy has its own event notification system that gets layered on top of SQLAlchemy.
# To do this, it tracks modifications to the SQLAlchemy session. This takes extra resources, so
# the option SQLALCHEMY_TRACK_MODIFICATIONS enables/disables the modification tracking system.
# Suggest disabling it if not in use to save system resources.
# To turn off the Flask-SQLAlchemy event system (and disable the warning):
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # use uuid as pk, use lambda to define an id generator
    id = db.Column('id', db.Text(length=36), default=lambda: str(
        uuid.uuid4()), primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    pic = db.Column(db.LargeBinary, nullable=True)


@app.route('/todos', methods=['GET'])
def home():
    rs = Todo.query.all()
    todo_list = []
    for todo in rs:
        t = {
            'id': todo.id,
            'title': todo.title,
            'complete': todo.complete,
        }

        try:
            t['img'] = b64encode(todo.pic).decode("utf-8")
        except Exception as e:
            print('>> error decoding image', e)

        todo_list.append(t)

    # transform blob to base64 for img tag data:uri
    # todo_list = [
    #     {
    #         'id': todo.id,
    #         'title': todo.title,
    #         'complete': todo.complete,
    #         'img': b64encode(todo.pic).decode("utf-8")
    #     } for todo in Todo.query.all()
    # ]
    return render_template('todos/home.html', todo_list=todo_list)


@app.route('/todos/add', methods=['POST'])
def add():
    title = request.form.get('title')

    file_err = None
    if 'pic' not in request.files:
        print('>> no file uploaded')
        flash('no file uploaded')
    else:
        file = request.files['pic']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('no file selected for upload')
            print('>> no file selected for upload')
        filename = secure_filename(file.filename)

        # check file is not as easy
        file_err = None
        # first try check browser content length if given
        if file.content_length:
            print('>> file content_length: ', file.content_length)
            if file.content_length > 1000000:
                file_err = 'file size is too large: ' + file.content_length
        else:
            # use seek and tell methods to get size without loading content
            # into memory
            pos = file.tell()
            file.seek(0, 2)  # seek to end
            size = file.tell()
            file.seek(pos)  # back to original position
            print('>> file size by seeking: ', size)
            if size > 1000000:
                # size_err = f'file size is too large: {size}'
                file_err = 'file size is too large'

    new_todo = Todo(title=title, complete=False)

    if file_err:
        flash(file_err)
        print(file_err)
    else:
        blob = file.read()
        # todo: be careful not to read too much data into memory
        # this is not considerred safe to be used for size check
        # size = len(blob)
        new_todo.pic = blob

    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/todos/update/<todo_id>', methods=['POST', 'PUT'])
def update(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id).first()
        new_title = request.form.get('title')
        new_complete = bool(request.form.get('complete'))
        if todo:
            todo.title = new_title
            todo.complete = new_complete
            db.session.commit()
    except Exception as e:
        print('Failed to update todo:', todo)
        print(e)
    return redirect('/todos')


# @app.route('/todos/delete/<int:todo_id>')
@app.route('/todos/delete/<todo_id>', methods=['POST', 'DELETE'])
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
    app.run(debug=True)
