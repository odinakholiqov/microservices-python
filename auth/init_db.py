import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (email, password) VALUES (?, ?)",
            ('odina', 'odina')
            )

connection.commit()
connection.close()
