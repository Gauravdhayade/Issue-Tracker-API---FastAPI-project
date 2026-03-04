from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, Index
from datetime import datetime
from app.core.database import Base
import enum

class StatusEnum(str, enum.Enum):
    Open = "Open"
    InProgress = "In Progress"
    Review = "Review"
    Done = "Done"

class PriorityEnum(str, enum.Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"
    Critical = "Critical"

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)

    status = Column(Enum(StatusEnum), default=StatusEnum.Open)
    priority = Column(Enum(PriorityEnum))

    project_id = Column(Integer, ForeignKey("projects.id"))
    reporter_id = Column(Integer, ForeignKey("users.id"))
    assignee_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Database Indexes (Performance Optimization)
Index("idx_issue_status", Issue.status)
Index("idx_issue_priority", Issue.priority)
Index("idx_issue_assignee", Issue.assignee_id)