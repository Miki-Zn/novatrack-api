import uuid
from pydantic import BaseModel, ConfigDict
from app.models.project_member import ProjectRole

class ProjectMemberCreate(BaseModel):
    user_id: uuid.UUID
    role: ProjectRole = ProjectRole.MEMBER

class ProjectMemberResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    user_id: uuid.UUID
    role: ProjectRole

    model_config = ConfigDict(from_attributes=True)