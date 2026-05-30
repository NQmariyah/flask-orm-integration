from flask import Flask, request, jsonify

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
		    "id":self.id,
		    "item": self.item,
		    "completed": self.completed
		}

todos = []

@app.route('/tasks', methods=['POST'])
def add_todos():
	if not request.json or not 'item' in request.json:
		abort(400, "Bad Request")

	item = request.json['item']
	new_todo = Todo(item)
	todos.append(new_todo)

	return jsonify(new_todo.to_dict()), 201


if __name__ == '__main__':
	app.run(debug=True)