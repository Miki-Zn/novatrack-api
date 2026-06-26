import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user
from app.models.task import TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService

from typing import Optional
import csv
import io
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task_service = TaskService(db)
    return task_service.create_task(task_in, current_user_id=current_user.id)

@router.get("/project/{project_id}", response_model=list[TaskResponse])
def read_project_tasks(
    project_id: uuid.UUID,
    status: Optional[TaskStatus] = None,
    search_query: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task_service = TaskService(db)
    return task_service.get_tasks_by_project(
        project_id=project_id, 
        current_user_id=current_user.id,
        skip=skip,
        limit=limit,
        status=status,
        search_query=search_query
    )

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: uuid.UUID,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task_service = TaskService(db)
    return task_service.update_task(task_id, task_in, current_user.id)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task_service = TaskService(db)
    task_service.delete_task(task_id, current_user.id)

@router.get("/project/{project_id}/export/csv")
def export_project_tasks_csv(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task_service = TaskService(db)
    tasks = task_service.get_tasks_by_project(project_id, current_user.id, skip=0, limit=1000)

    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["ID", "Title", "Description", "Status"])
    
    for task in tasks:
        writer.writerow([str(task.id), task.title, task.description or "", task.status.value])
        
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=project_{project_id}_tasks.csv"}
    )