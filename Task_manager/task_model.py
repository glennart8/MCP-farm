from pydantic import BaseModel, Field


class Task(BaseModel):
    title: str
    priority: int=Field(gt=0, le=6)
    description: str = ""
    preparations: str = ""
    practical_desc: str = ""
    grants: str = "" # bidrag