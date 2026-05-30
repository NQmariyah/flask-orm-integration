from flask import request, jsonify, abort
from todomodels import app, Todo, db


@app.route('/tasks', methods=['POST'])
def add_todos():
    if not request.json or 'item' not in request.json:
        abort(400, "Bad Request")

    item = request.json['item']

    new_todo = Todo(item=item)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify(new_todo.to_dict()), 201


@app.route('/tasks', methods=['GET'])
def get_todos():
    tasks = Todo.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_todo_by_id(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, item, completed FROM todo WHERE id = ?",
                   (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        abort(404, f"Todo ID: {task_id} Not Found")

    task = Todo(row['id'], row['item'], bool(row['completed']))

    return jsonify(task.to_dict()), 200


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

    cursor.execute("UPDATE todo SET item = ?, completed = ? WHERE id = ?",
                   (item, completed, task_id))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, f"Todo ID: {task_id} Not Found")

    conn.close()

    task = Todo(task_id, item, completed)

    return jsonify(task.to_dict()), 200


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


if __name__ == '__main__':
    app.run(debug=True)
