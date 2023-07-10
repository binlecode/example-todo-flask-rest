# provides REST endpoints for CRUDs


from werkzeug.exceptions import HTTPException
import json
import uuid
from flask import Flask, request, Response
from rest import app

from . import todo_dao


@app.route("/")
def hello_world():
    return "Hello Todo App (REST + Sql)"


@app.route("/todos", methods=["GET"])
def get_todos():
    todo_list, count = todo_dao.list()
    return {"todo_list": todo_list, "count": len(todo_list)}


@app.route("/todos/<id>", methods=["GET"])
def get_todo(id: str):
    todo = todo_dao.get(id)
    return {"todo": todo}


# Example call:
# curl -X POST http://127.0.0.1:5000/todos -d '{"title": "Implement POST endpoint"}' -H 'Content-Type: application/json'
#
@app.route("/todos", methods=["POST"])
def add_todo():
    todo_json = request.get_json()
    title = todo_json.get("title")  # todo: validation
    # generate pk id with uuid4
    id = str(uuid.uuid4())
    todo = todo_dao.add(id, title)
    return {"todo": todo}, 201


# Example call:
# curl -X PUT http://127.0.0.1:5000/todos/001 -d '{"title": "make a cup of tea"}' -H 'Content-Type: application/json'
#
@app.route("/todos/<id>", methods=["PUT"])
def update_todo(id: str):
    todo_json = request.get_json()
    title = todo_json.get("title")  # todo: validation
    complete = todo_json.get("complete")
    if complete is not None:
        complete = bool(complete)

    todo = todo_dao.get(id)
    if todo:
        if title:
            todo["title"] = title
        if complete is not None:
            todo["complete"] = complete
        return todo_dao.update(todo)

    return {"message": "todo not found"}, 204


# Example call:
# curl -X DELETE http://127.0.0.1:5000/todos/90e0a8a4-0ac0-4abc-8871-259025d46c00 -H 'Content-Type: application/json'
#
@app.route("/todos/<id>", methods=["DELETE"])
def delete_todo(id: str):
    todo_dao.delete(id)
    return {"message": "ok"}, 200


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
