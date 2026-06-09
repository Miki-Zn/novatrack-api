from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password
from app.services.user_service import UserService

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.user_service.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user