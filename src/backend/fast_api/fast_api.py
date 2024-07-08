from typing import List

from fastapi import FastAPI, HTTPException, Request, Response

from src.backend.fast_api.model.task import Task
from src.backend.fast_api.service import task_service

app = FastAPI()


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return task_service.get_all_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task_by_id(task_id: int):
    task = task_service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(request: Request):
    task_data = await request.json()
    if "title" not in task_data:
        raise HTTPException(status_code=400, detail="Title is required")
    task = Task(
        title=task_data['title'],
        description=task_data.get('description', ""),
        done=False
    )
    new_task = await task_service.create_task(task)
    return new_task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, request: Request):
    task_data = await request.json()
    task = task_service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if "title" in task_data and not isinstance(task_data["title"], str):
        raise HTTPException(status_code=400, detail="Invalid title")
    if "description" in task_data and not isinstance(task_data["description"], str):
        raise HTTPException(status_code=400, detail="Invalid description")
    if "done" in task_data and not isinstance(task_data["done"], bool):
        raise HTTPException(status_code=400, detail="Invalid done")
    task.title = task_data.get("title", task.title)
    task.description = task_data.get("description", task.description)
    task.done = task_data.get("done", task.done)

    updated_task = await task_service.update_task(task)
    return updated_task


@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int):
    task = task_service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await task_service.delete_task(task_id)
    return Response(status_code=204, content='{"result": true}')
