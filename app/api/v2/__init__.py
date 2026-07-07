import uuid
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.models.task import TaskStatus
from app.services.task_service import TaskService

router = APIRouter()

@router.get("/project/{project_id}")
def read_project_tasks_v2(
    project_id: uuid.UUID,
    status: Optional[TaskStatus] = None,
    search_query: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task_service = TaskService(db)
    tasks = task_service.get_tasks_by_project(
        project_id=project_id, 
        current_user_id=current_user.id,
        skip=skip,
        limit=limit,
        status=status,
        search_query=search_query
    )
    
    return {
        "meta": {
            "version": "2.0",
            "total_returned": len(tasks),
            "project_id": str(project_id)
        },
        "data": tasks
    }