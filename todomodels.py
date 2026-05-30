import os
import sqlite3

DATABASE_NAME = 'todoapp.db'
DATABASE_PATH = os.path.join(app.instance_path, DATABASE_NAME)

# berikut adalah fungsi-fungsi yang digunakan 
# untuk akses DATABASE menggunakan NATIVE

def get_db_connection():
	conn = sqlite3.connect(DATABASE_PATH)
	conn.row_factory = sqlite3.Row
	return conn


def init_db():
	os.makedirs(app.instance_path, exist_ok=True)

	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS todo (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			item TEXT NOT NULL,
			completed INTEGER NOT NULL DEFAULT 0
		)
	''')
	conn.commit()
	conn.close()

with app.app_context():
	init_db()