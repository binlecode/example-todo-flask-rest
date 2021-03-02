# model.py
#

from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy
import uuid


db = SQLAlchemy()


class Todo(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # use uuid as pk, use lambda to define an id generator
    id = db.Column('id', db.Text(length=36), default=lambda: str(
        uuid.uuid4()), primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    pic = db.Column(db.LargeBinary, nullable=True)
