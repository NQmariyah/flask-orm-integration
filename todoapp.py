from flask import Flask, request, jsonify

app = Flask(__name__)


class Todo:
	next_id = 1

	def __init__(self, title):
		self.id = next_id
		self.title = title
		self.completed = False

		next_id += 1

	def to_dict(self):
		return {
		    "id":self.id,
		    "title": self.title,
		    "completed": self.completed
		}

if __name__ == '__main__':
	app.run(debug=True)