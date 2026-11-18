
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Task Management API",
    description="A simple REST API for managing tasks",
    version="1.0.0"
)

# In-memory task storage
tasks = []
next_id = 1


class TaskCreate(BaseModel):
    title: str
    completed: bool = False


@app.get("/")
def home():
    return {
        "message": "Welcome to Task Management API",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/todos")
def get_tasks():
    return tasks


@app.post("/todos", status_code=201)
def create_task(task: TaskCreate):
    global next_id

    new_task = {
        "id": next_id,
        "title": task.title,
        "completed": task.completed
    }

    tasks.append(new_task)
    next_id += 1

    return new_task


@app.get("/todos/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
