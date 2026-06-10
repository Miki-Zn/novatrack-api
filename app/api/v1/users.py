from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_active_user, RoleChecker
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    return user_service.create_user(user_in)

@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user

allow_admin = RoleChecker([UserRole.ADMIN])

@router.get("/admin-panel")
def read_admin_data(
    current_user: User = Depends(allow_admin)
):
    return {
        "message": f"Welcome to the secret admin panel, {current_user.full_name}!",
        "confidential_data": "Here is the sensitive company data."
    }