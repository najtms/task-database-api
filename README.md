```text
 ______ _      ______            _       ___  _____
|  ___| |     | ___ \          | |     / _ \|_   _|
| |_  | |_   _| |_/ /__ _ _ __ | | __ / /_\ \ | |
|  _| | | | | |    // _` | '_ \| |/ / |  _  | | |
| |   | | |_| | |\ \ (_| | | | |   <  | | | |_| |_
\_|   |_|\__,_|_\ \__,_|_| |_|_|\_\ \_| |_/\___/
          __/ |
         |___/
```

# Task API

A simple CRUD REST API built with **FastAPI** and SQLite for the FlyRank Backend Internship assignment.

---

## Features

* Create tasks
* Read all tasks
* Read a task by ID
* Update tasks
* Delete tasks
* SQLite database persistence
* Automatic database creation
* Automatic seeding with example tasks
* Automatic Swagger UI documentation

---

## Tech Stack

* Python 3
* FastAPI
* Uvicorn
* SQLite

---

## Requirements

* Python 3.10+
* FastAPI
* Uvicorn

---

# Database

## Why SQLite?

SQLite was chosen because:

* It uses a single database file
* It requires zero setup or external database server
* Data survives application restarts
* It is lightweight and easy to distribute with the project

The application automatically creates the database when it starts.

The database file is:

```
tasks.db
```

It is created automatically and is usually **git-ignored**, so every new clone creates its own fresh database with the initial seeded data.

---

## Database Initialization

When the application starts:

1. `tasks.db` is created if it does not exist
2. The `tasks` table is created automatically
3. Three example tasks are inserted if the database is empty

Example seeded tasks:

| id | title  | done  |
| -- | ------ | ----- |
| 1  | Task 0 | true  |
| 2  | Task 1 | true  |
| 3  | Task 2 | false |

No manual database setup is required.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/najtms/task-database-api.git
cd task-api
```

Install dependencies:

```bash
pip install fastapi uvicorn
```

---

# Run the Project

Start the server with:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

---

# API Endpoints

| Method | Endpoint      | Description     |
| ------ | ------------- | --------------- |
| GET    | `/`           | API information |
| GET    | `/health`     | Health check    |
| GET    | `/tasks`      | Get all tasks   |
| GET    | `/tasks/{id}` | Get task by ID  |
| POST   | `/tasks`      | Create task     |
| PUT    | `/tasks/{id}` | Update task     |
| DELETE | `/tasks/{id}` | Delete task     |

---

# Example curl Output

```bash
curl -i http://localhost:8000/tasks
```

Example response:

```http
HTTP/1.1 200 OK
content-type: application/json

[
  {
    "id":1,
    "title":"Task 0",
    "done":true
  },
  {
    "id":2,
    "title":"Task 1",
    "done":true
  },
  {
    "id":3,
    "title":"Task 2",
    "done":false
  }
]
```

---

# Swagger UI

![Swagger UI](images/Swagger.png)

---

# Database Browser Screenshot

Database opened using **DB Browser for SQLite**:

![SQLite Database](images/gui.png)

---

# Example SQL Query

Example query executed in DB Browser for SQLite:

```sql
SELECT * FROM tasks;
```

Result:

| id | title  | done |
| -- | ------ | ---- |
| 1  | Task 0 | 1    |
| 2  | Task 1 | 1    |
| 3  | Task 2 | 0    |

---

# Project Structure

```
task-api/
│── main.py
│── tasks.db
│── README.md
|── .gitignore
└── images/
    ├── Swagger.png
    └── Database.png
```

Note:

`tasks.db` is generated automatically when the application starts and should normally be excluded from version control.

---

## Author

**Muhamad Assaad**

FlyRank Backend Internship Assignment

```
```
