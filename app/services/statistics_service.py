import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.project import Project
from app.models.task import Task, TaskStatus
from app.schemas.statistics import DashboardStats, TaskStatusCounts

class StatisticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_dashboard_stats(self, user_id: uuid.UUID) -> DashboardStats:
        total_projects = self.db.query(func.count(Project.id)).filter(Project.owner_id == user_id).scalar() or 0

        tasks_query = self.db.query(Task.status, func.count(Task.id)).join(Project).filter(Project.owner_id == user_id).group_by(Task.status).all()

        task_stats_dict = {status.value: 0 for status in TaskStatus}
        total_tasks = 0

        for status, count in tasks_query:
            task_stats_dict[status.value] = count
            total_tasks += count

        task_status_counts = TaskStatusCounts(**task_stats_dict)

        return DashboardStats(
            total_projects=total_projects,
            total_tasks=total_tasks,
            task_stats=task_status_counts
        )