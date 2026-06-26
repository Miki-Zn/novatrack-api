import uuid
from sqlalchemy.orm import Session
from sqlalchemy import or_
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

    def get_tasks_by_project(
        self, 
        project_id: uuid.UUID, 
        current_user_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        status: str | None = None,
        search_query: str | None = None
    ) -> list[Task]:
        self.project_service.get_project_by_id(project_id, current_user_id)
        
        query = self.db.query(Task).filter(Task.project_id == project_id)
        
        if status:
            query = query.filter(Task.status == status)
            
        if search_query:
            search_term = f"%{search_query}%"
            query = query.filter(
                or_(
                    Task.title.ilike(search_term),
                    Task.description.ilike(search_term)
                )
            )
            
        return query.offset(skip).limit(limit).all()

    def get_task_by_id(self, task_id: uuid.UUID, current_user_id: uuid.UUID) -> Task:
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        self.project_service.get_project_by_id(task.project_id, current_user_id)
        return task

    def update_task(self, task_id: uuid.UUID, task_in: TaskUpdate, current_user_id: uuid.UUID) -> Task:
        db_task = self.get_task_by_id(task_id, current_user_id)
        update_data = task_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete_task(self, task_id: uuid.UUID, current_user_id: uuid.UUID):
        db_task = self.get_task_by_id(task_id, current_user_id)
        self.db.delete(db_task)
        self.db.commit()