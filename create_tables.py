import sqlite3

c = sqlite3.connect('users.db')
cu = c.cursor()

table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cu.execute(table)

c.commit()
c.close()