from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.config import settings
from app.core.security import create_access_token, create_password_reset_token, verify_password_reset_token, get_password_hash
from app.schemas.token import Token
from app.services.auth_service import AuthService
from app.core.rate_limit import limiter
from app.schemas.auth import ForgotPasswordRequest, ResetPasswordRequest
from app.models.user import User
from app.services.email_service import send_welcome_email

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
@limiter.limit("5/minute")
def login_access_token(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    user = auth_service.authenticate(email=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/forgot-password")
def forgot_password(
    request_data: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == request_data.email).first()
    if not user:
        return {"message": "If this email is registered, a reset link has been sent."}
        
    reset_token = create_password_reset_token(email=user.email)
    
    reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
    
    background_tasks.add_task(
        send_welcome_email, 
        email_to=user.email, 
        name=f"Reset Password Link: {reset_link}"
    )
    
    return {"message": "If this email is registered, a reset link has been sent."}

@router.post("/reset-password")
def reset_password(
    request_data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    email = verify_password_reset_token(request_data.token)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
        
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    user.hashed_password = get_password_hash(request_data.new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}