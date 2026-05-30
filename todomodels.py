import os
import sqlite3
from flask import Flask

app = Flask(__name__)

DATABASE_NAME = 'todoapp.db'
DATABASE_PATH = os.path.join(app.instance_path, DATABASE_NAME)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# berikut adalah definisi model yang digunakan dalam ORM
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "item": self.item,
            "completed": bool(self.completed)
        }




with app.app_context():
    db.create_all()
