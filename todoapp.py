from flask import request, jsonify, abort
from todomodels import app, Todo, db, jwt
from flask-jwt-extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


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
    task = Todo.query.get(task_id)

    if task is None:
        abort(404, f"Todo ID: {task_id} Not Found")

    return jsonify(task.to_dict()), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_todo(task_id):
    if (not request.json
            or 'item' not in request.json
            or 'completed' not in request.json):
        abort(400, "Bad Request")

    task = Todo.query.get(task_id)

    if task is None:
        abort(404, f"Todo ID: {task_id} Not Found")

    task.item = request.json['item']
    task.completed = request.json['completed']

    db.session.commit()

    return jsonify(task.to_dict()), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_todo(task_id):
    task = Todo.query.get(task_id)

    if task is None:
        abort(404, f"Todo ID: {task_id} Not Found")

    db.session.delete(task)
    db.session.commit()

    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
