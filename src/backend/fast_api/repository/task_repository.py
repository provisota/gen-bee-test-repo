from typing import List, Optional

from src.backend.fast_api.model.task import Task

_tasks = [
    Task(id=1, title="Learn Python", description="Study the basics of Python programming."),
    Task(id=2, title="Build a REST API", description="Create a simple REST API using FastAPI.")
]


def get_all_tasks() -> List[Task]:
    return _tasks


def get_task_by_id(task_id: int) -> Optional[Task]:
    return next((task for task in _tasks if task.id == task_id), None)


async def create_task(task: Task) -> Task:
    task.id = _tasks[-1].id + 1 if _tasks else 1

    _tasks.append(task)
    return task


async def update_task(updated_task: Task) -> Optional[Task]:
    for existing_task in _tasks:
        if existing_task.id == updated_task.id:
            existing_task.title = updated_task.title
            existing_task.description = updated_task.description
            existing_task.done = updated_task.done
            return existing_task
    return None


async def delete_task(task_id: int) -> None:
    global _tasks
    _tasks = [task for task in _tasks if task.id != task_id]


def delete_all_tasks() -> None:
    global _tasks
    _tasks = []
