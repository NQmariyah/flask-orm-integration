from flask import request, jsonify, abort
from todomodels import app, get_db_connection


class Todo:
    def __init__(self, id, item, completed=False):
        self.id = id
        self.item = item
        self.completed = completed

    def to_dict(self):
        return {
            "id": self.id,
            "item": self.item,
            "completed": self.completed
        }


@app.route('/tasks', methods=['POST'])
def add_todos():
    if not request.json or 'item' not in request.json:
        abort(400, "Bad Request")

    item = request.json['item']
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO todo (item, completed) VALUES (?,0)", (item,))
    conn.commit()

    new_id = cursor.lastrowid
    conn.close()

    new_todo = Todo(new_id, item)

    return jsonify(new_todo.to_dict()), 201


@app.route('/tasks', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, item, completed FROM todo")
    rows = cursor.fetchall()
    conn.close()

    tasks = []
    for row in rows:
        tasks.append(Todo(row['id'], row['item'], bool(row['completed'])).to_dict())
    # tasks = [todo.to_dict() for todo in todos]
    return jsonify(tasks), 200


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_todo_by_id(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, item, completed FROM todo WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        abort(404, f"Todo ID: {task_id} Not Found")

    task = Todo(row['id'], row['item'], bool(row['completed']))

    return jsonify(task.to_dict()), 200

    # for todo in todos:
    #     if todo.id == task_id:
    #         return jsonify(todo.to_dict()), 200

    # return jsonify({"error": f"Todo ID: {task_id} Not Found"}), 404


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_todo(task_id):
    if (not request.json
            or 'item' not in request.json
            or 'completed' not in request.json):
        abort(400, "Bad Request")

    item = request.json['item']
    completed = request.json['completed']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE todo SET item = ?, completed = ? WHERE id = ?", (item, completed, task_id))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, f"Todo ID: {task_id} Not Found")

    conn.close()

    task = Todo(task_id, item, completed)

    return jsonify(task.to_dict()), 200


    # for todo in todos:
    #     if todo.id == task_id:
    #         todo.item = request.json['item']
    #         todo.completed = request.json['completed']
    #         return jsonify(todo.to_dict()), 201

    # return jsonify({"error": f"Todo ID: {task_id} Not Found"}), 404


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_todo(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM todo WHERE id = ?", (task_id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, f"Todo ID:{task_id} Not Found")

    conn.close()

    return '', 204
    # for todo in todos:
    #     if todo.id == task_id:
    #         todos.remove(todo)
    #         return '', 204


if __name__ == '__main__':
    app.run(debug=True)
