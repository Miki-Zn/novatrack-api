import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.schemas.project_member import ProjectMemberCreate, ProjectMemberResponse

router = APIRouter()

@router.post("/project/{project_id}/members", response_model=ProjectMemberResponse)
def add_project_member(
    project_id: uuid.UUID,
    member_in: ProjectMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions or project not found")

    existing_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == member_in.user_id
    ).first()
    
    if existing_member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a member of this project")

    new_member = ProjectMember(
        project_id=project_id,
        user_id=member_in.user_id,
        role=member_in.role
    )
    
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    
    return new_member