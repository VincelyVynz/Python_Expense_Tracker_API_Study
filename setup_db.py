import sqlite3

conn = sqlite3.connect('expense_tracker.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
id INTEGER PRIMARY KEY AUTOINCREMENT,
item TEXT,
amount REAL,
category TEXT,
date TEXT)
""")
conn.commit()
conn.close()