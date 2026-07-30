from fastapi import FastAPI, Request, HTTPException
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

@app.put("/tasks/{id}", summary="Update a task")
async def update_task(id: int, req: Request):

    task = None
    for t in tasks:
        if t["id"] == id:
            task = t
            break

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )

    try:
        data = await req.json()
    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON"
        )

    if not data:
        raise HTTPException(
            status_code=400,
            detail="Request body cannot be empty"
        )

    if "title" in data:
        if data["title"].strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Title cannot be empty"
            )
        task["title"] = data["title"]

    if "done" in data:
        task["done"] = data["done"]

    return task


    from fastapi import Response

@app.delete("/tasks/{id}", status_code=204, summary="Delete a task")
async def delete_task(id: int):

    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return Response(status_code=204)

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )