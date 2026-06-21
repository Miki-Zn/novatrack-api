from pydantic import BaseModel

class TaskStatusCounts(BaseModel):
    todo: int = 0
    in_progress: int = 0
    done: int = 0

class DashboardStats(BaseModel):
    total_projects: int
    total_tasks: int
    task_stats: TaskStatusCounts