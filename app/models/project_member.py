import uuid
from enum import Enum
from sqlalchemy import ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class ProjectRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"

class ProjectMember(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[ProjectRole] = mapped_column(SQLEnum(ProjectRole), default=ProjectRole.MEMBER, nullable=False)

    user = relationship("User")
    project = relationship("Project")