# serve todos endpoints by sql queries no models
# provides REST endpoints instead of html


from rest import db
from rest import app
from werkzeug.exceptions import HTTPException
import json
import uuid
from flask import Flask, request, Response
import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))


# reuse the sqlite3 db created by todos.py app
DB_PATH = "./todos.db"


@app.route("/")
def hello_world():
    return "Hello Todo App (REST + Sql)!"


@app.route("/todos")
def get_todos():
    try:
        # conn = sqlite3.connect(DB_PATH)
        conn = db.get_db()

        # Once a connection has been established, we use the cursor
        # object to execute queries
        c = conn.cursor()
        c.execute("select * from todo")
        todo_list = [dict(row) for row in c.fetchall()]

        return {"todo_list": todo_list, "count": len(todo_list)}

        # or dump todo_list to json explicitly
        # return Response(json.dumps(todo_list), mimetype='application/json')
    except Exception as e:
        print("Error: ", e)
        return {}


# Example call:
# curl -X POST http://127.0.0.1:5000/todos -d '{"title": "Implement POST endpoint"}' -H 'Content-Type: application/json'
#
@app.route("/todos", methods=["POST"])
def add_todo():
    # try:
    # Get item from the POST body
    todo_json = request.get_json()
    title = todo_json["title"]  # todo: validation

    # generate pk id with uuid4
    id = str(uuid.uuid4())
    conn = db.get_db()
    c = conn.cursor()
    c.execute("insert into todo(id, title) values(?, ?)", (id, title))
    conn.commit()
    return {"data": {"id": id, "title": title, "complete": False}}
    # except Exception as e:
    #     print('Error: ', e)
    #     return {}


@app.errorhandler(HTTPException)
def handle_exception(e):
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response
    # return Response(err_json, mimetype='application/json', status=500)
