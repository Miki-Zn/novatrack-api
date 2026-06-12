import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project_service import ProjectService

router = APIRouter()

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    project_service = ProjectService(db)
    return project_service.create_project(project_in, owner_id=current_user.id)

@router.get("/", response_model=list[ProjectResponse])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    project_service = ProjectService(db)
    return project_service.get_user_projects(owner_id=current_user.id, skip=skip, limit=limit)

@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    project_service = ProjectService(db)
    return project_service.get_project_by_id(project_id=project_id, owner_id=current_user.id)