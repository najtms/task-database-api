import sqlite3

con = sqlite3.connect("task.db")


#
cur = con.cursor()
#
## Creation of table
cur.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, done BOOLEAN)")

cur.execute("SELECT COUNT(*) FROM tasks")
COUNT = cur.fetchone()[0]

if COUNT ==0:
    cur.executemany("INSERT INTO tasks(title, done) VALUES(?, ?)", [
        ("Task 0", True),
        ("Task 1", True),
        ("Task 2", False)
    ])

con.commit()

cur.execute("SELECT * FROM tasks")
tasks = cur.fetchall()


for task in tasks:
    print(task)

con.close()