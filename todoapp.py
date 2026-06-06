from flask import request, jsonify, abort
from todomodels import app, Todo, db, User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.json

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Field username dan password tidak ditemukan."}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username sudah digunakan."}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User berhasil didaftarkan."}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username dan password tidak ditemukan."}), 400

    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Username atau password salah."}), 401

@app.route('/tasks', methods=['POST'])
@jwt_required()
def add_todos():
    current_user = get_jwt_identity()

    if not request.json or 'item' not in request.json:
        abort(400, "Bad Request")

    item = request.json['item']

    new_todo = Todo(item=item, user_id=current_user)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify(new_todo.to_dict()), 201


@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_todos():
    current_user = get_jwt_identity()

    tasks = Todo.query.filter_by(user_id=current_user)
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
