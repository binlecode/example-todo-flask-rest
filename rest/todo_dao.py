from . import db


def list(options={}):
    conn = db.get_db()
    # Once a connection has been established, we use the cursor
    # object to execute queries
    c = conn.cursor()
    c.execute("select * from todo")
    todo_list = [dict(row) for row in c.fetchall()]

    return todo_list, len(todo_list)


def get(id: str):
    conn = db.get_db()
    c = conn.cursor()
    c.execute("select * from todo where id = ? limit 1", (id,))
    todo_list = [dict(row) for row in c.fetchall()]
    if todo_list:
        return todo_list[0]
    return None


def add(id, title):
    conn = db.get_db()
    c = conn.cursor()
    c.execute("insert into todo(id, title, complete) values(?, ?, 0)", (id, title))
    conn.commit()
    return {"id": id, "title": title, "complete": False}


def update(todo: dict):
    conn = db.get_db()
    c = conn.cursor()
    c.execute(
        "update todo set title = ?, complete = ? where id = ?",
        (todo["title"], todo["complete"], todo["id"]),
    )
    conn.commit()
    return todo


def delete(id: str):
    conn = db.get_db()
    c = conn.cursor()
    c.execute("delete from todo where id = ?", (id,))
    conn.commit()
    return id
