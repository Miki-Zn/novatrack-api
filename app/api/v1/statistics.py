from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.schemas.statistics import DashboardStats
from app.services.statistics_service import StatisticsService

router = APIRouter()

@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    stats_service = StatisticsService(db)
    return stats_service.get_user_dashboard_stats(current_user.id)