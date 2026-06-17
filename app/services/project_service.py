import uuid
import json
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.project import Project
from app.schemas.project import ProjectCreate
from app.core.cache import redis_client

class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    def create_project(self, project_in: ProjectCreate, owner_id: uuid.UUID) -> Project:
        db_project = Project(
            title=project_in.title,
            description=project_in.description,
            owner_id=owner_id
        )
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        
        redis_client.delete(f"projects:{owner_id}:0:100")
        
        return db_project

    def get_user_projects(self, owner_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[Project]:
        cache_key = f"projects:{owner_id}:{skip}:{limit}"
        cached_data = redis_client.get(cache_key)
        
        if cached_data:
            return json.loads(cached_data)

        projects = self.db.query(Project).filter(Project.owner_id == owner_id).offset(skip).limit(limit).all()
        
        projects_dict = [
            {"id": str(p.id), "title": p.title, "description": p.description, "owner_id": str(p.owner_id)}
            for p in projects
        ]
        redis_client.setex(cache_key, 300, json.dumps(projects_dict))
        
        return projects

    def get_project_by_id(self, project_id: uuid.UUID, owner_id: uuid.UUID) -> Project:
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        if project.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return project