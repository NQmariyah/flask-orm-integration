from flask import Flask, request, jsonify

app = Flask(__name__)


class Todo:
	next_id = 1

	def __init__(self, item):
		self.id = next_id
		self.item = item
		self.completed = False

		next_id += 1

	def to_dict(self):
		return {
		    "id":self.id,
		    "item": self.item,
		    "completed": self.completed
		}


if __name__ == '__main__':
	app.run(debug=True)