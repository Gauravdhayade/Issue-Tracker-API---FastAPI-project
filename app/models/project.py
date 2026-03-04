from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from datetime import datetime
from app.core.database import Base
import enum

class VisibilityEnum(str, enum.Enum):
    Private = "Private"
    Public = "Public"

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    project_key = Column(String(50), unique=True)
    description = Column(String(500))
    visibility = Column(Enum(VisibilityEnum))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)