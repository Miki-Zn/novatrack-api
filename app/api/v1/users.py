import os
import uuid
import shutil
from fastapi import APIRouter, Depends, status, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_active_user, RoleChecker
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.services.email_service import send_welcome_email

router = APIRouter()

allow_admin = RoleChecker([UserRole.ADMIN])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    new_user = user_service.create_user(user_in)
    
    user_name = new_user.full_name or "New User"
    background_tasks.add_task(send_welcome_email, email_to=new_user.email, name=user_name)
    
    return new_user

@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user

@router.get("/admin-panel")
def read_admin_data(
    current_user: User = Depends(allow_admin)
):
    return {
        "message": f"Welcome to the secret admin panel, {current_user.full_name}!",
        "confidential_data": "Here is the sensitive company data."
    }

@router.post("/avatar", response_model=UserResponse)
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    os.makedirs("static/avatars", exist_ok=True)
    
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join("static/avatars", unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    current_user.avatar_url = f"/static/avatars/{unique_filename}"
    db.commit()
    db.refresh(current_user)
    
    return current_user