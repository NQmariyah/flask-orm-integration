from flask import Flask, request, jsonify, abort

app = Flask(__name__)


class Todo:
    next_id = 1

    def __init__(self, item):
        self.id = Todo.next_id
        self.item = item
        self.completed = False

        Todo.next_id += 1

    def to_dict(self):
        return {
            "id": self.id,
            "item": self.item,
            "completed": self.completed
        }


todos = []


@app.route('/tasks', methods=['POST'])
def add_todos():
    if not request.json or 'item' not in request.json:
        abort(400, "Bad Request")

    item = request.json['item']
    new_todo = Todo(item)
    todos.append(new_todo)

    return jsonify(new_todo.to_dict()), 201


@app.route('/tasks', methods=['GET'])
def get_todos():
    tasks = [todo.to_dict() for todo in todos]
    return jsonify(tasks), 200


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_todo_by_id(task_id):
    for todo in todos:
        if todo.id == task_id:
            return jsonify(todo.to_dict()), 200

    return jsonify({"error": f"Todo ID: {task_id} Not Found"}), 404


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_todo(task_id):
    if (not request.json
            or 'item' not in request.json
            or 'completed' not in request.json):
        abort(400, "Bad Request")

    for todo in todos:
        if todo.id == task_id:
            todo.item = request.json['item']
            todo.completed = request.json['completed']
            return jsonify(todo.to_dict()), 201

    return jsonify({"error": f"Todo ID: {task_id} Not Found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
