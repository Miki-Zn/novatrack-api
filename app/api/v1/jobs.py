import uuid
from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.worker.tasks import process_heavy_report

router = APIRouter()

@router.post("/generate-report/{project_id}")
def trigger_report_generation(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user)
):
    task = process_heavy_report.delay(str(project_id), current_user.email)
    return {"task_id": task.id, "message": "Report generation started in the background"}