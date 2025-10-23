from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    title: str
    priority: int
    description: Optional[str] = None
    preparations: Optional[str] = None
    practical_desc: Optional[str] = None
    grants: Optional[str] = None


class Observation(BaseModel):
    tasks: list[Task]


class Action(BaseModel):
    type: str          # "add", "update", "none"
    index: Optional[int] = None
    task: Optional[Task] = None
    info: Optional[str] = None
