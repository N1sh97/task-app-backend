from pydantic import BaseModel
from typing import Optional


class CreateTask (BaseModel):
    title: str
    task_status: str


class TaskResponse(BaseModel):
    id: int
    title: str
    task_status: str

    model_config = {"from_attributes": True}


class UpdateTask (BaseModel):
    title: Optional[str] = None
    task_status: Optional[str] = None
