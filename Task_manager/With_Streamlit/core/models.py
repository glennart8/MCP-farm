from typing import Optional
from pydantic import BaseModel

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
    type: str           # "add", "update", "delete", "none"
    index: Optional[int] = None
    task: Optional[Task] = None
    info: Optional[str] = None
