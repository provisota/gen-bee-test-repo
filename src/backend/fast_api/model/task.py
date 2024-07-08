from typing import Optional

from pydantic import BaseModel


class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = ""
    done: bool = False
