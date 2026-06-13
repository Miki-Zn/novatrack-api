import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.task import TaskStatus

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO

class TaskCreate(TaskBase):
    project_id: uuid.UUID
    assignee_id: Optional[uuid.UUID] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    assignee_id: Optional[uuid.UUID] = None

class TaskResponse(TaskBase):
    id: uuid.UUID
    project_id: uuid.UUID
    assignee_id: Optional[uuid.UUID] = None

    model_config = ConfigDict(from_attributes=True)