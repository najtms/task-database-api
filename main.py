from fastapi import FastAPI, Request, HTTPException, Response
from pydantic import BaseModel,field_validator
import sqlite3
app = FastAPI()

################################################################################
#DATABASE
tasks = []
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





#####################################################################################


@app.get("/test")
async def test():
    return {}

###############################################################################
@app.get("/", summary="API information")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health",summary="Check API health")
async def health():
    return {"status": "ok"}
###############################################################################

###############################################################################
@app.get("/tasks", summary="Get all tasks")
async def get_tasks():
    cur.execute("SELECT * FROM tasks")
    taskx = cur.fetchall()
    return taskx


@app.get("/tasks/{id}", summary="Get task by ID")
async def get_task_by_id(id: int):
    id_valued = cur.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    task = id_valued.fetchone()
    if task:
        return task
    return {"error": f"Task {id} not found"}

###############################################################################
class Task(BaseModel):
    title: str

    @field_validator("title")
    def title_not_empty(cls, value):
        if value.strip() == "":
            raise ValueError("Title cannot be empty")

        return value


@app.post("/tasks", status_code=201)
async def create_task(task: Task):

    cur.execute(
        "INSERT INTO tasks(title, done) VALUES(?, ?)",
        (task.title, False)
    )

    con.commit()

    return task

###############################################################################
from pydantic import BaseModel, field_validator


class UpdateTask(BaseModel):
    title: str
    done: bool

    @field_validator("title")
    def title_not_empty(cls, value):
        if value.strip() == "":
            raise ValueError("Title cannot be empty")
        return value


@app.put("/tasks/{id}", summary="Update a task")
async def update_task(id: int, req: UpdateTask):

    cur.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    task = cur.fetchone()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )

    cur.execute(
        """
        UPDATE tasks 
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (req.title, req.done, id)
    )

    con.commit()

    return {
        "id": id,
        "title": req.title,
        "done": req.done
    }




@app.delete("/tasks/{id}", status_code=204, summary="Delete a task")
async def delete_task(id: int):
    cur.execute("DELETE FROM tasks WHERE id = ?", (id,))

    if cur.rowcount > 0:
        return Response(status_code=204)

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )