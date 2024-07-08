from typing import Optional, List

from src.backend.fast_api.model.task import Task
from src.backend.fast_api.repository import task_repository


def get_all_tasks() -> List[Task]:
    return task_repository.get_all_tasks()


def get_task_by_id(task_id: int) -> Optional[Task]:
    return task_repository.get_task_by_id(task_id)


async def create_task(task: Task) -> Task:
    return await task_repository.create_task(task)


async def update_task(task: Task) -> Optional[Task]:
    return await task_repository.update_task(task)


async def delete_task(task_id: int):
    await task_repository.delete_task(task_id)
