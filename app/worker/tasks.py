import time
from app.core.celery_app import celery_app

@celery_app.task(name="process_heavy_report")
def process_heavy_report(project_id: str, user_email: str):
    time.sleep(10)
    return {"project_id": project_id, "status": f"Report generated and sent to {user_email}"}