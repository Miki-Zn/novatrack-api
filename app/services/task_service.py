import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.project_service import ProjectService

class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.project_service = ProjectService(db)

    def create_task(self, task_in: TaskCreate, current_user_id: uuid.UUID) -> Task:
        self.project_service.get_project_by_id(task_in.project_id, current_user_id)
        
        db_task = Task(**task_in.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_tasks_by_project(self, project_id: uuid.UUID, current_user_id: uuid.UUID) -> list[Task]:
        self.project_service.get_project_by_id(project_id, current_user_id)
        
        return self.db.query(Task).filter(Task.project_id == project_id).all()