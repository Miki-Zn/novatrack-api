import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: uuid.UUID
    owner_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)