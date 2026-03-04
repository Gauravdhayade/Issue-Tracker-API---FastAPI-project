from pydantic import BaseModel
from app.models.issue import StatusEnum, PriorityEnum

class IssueCreate(BaseModel):
    title: str
    description: str
    priority: PriorityEnum
    assignee_id: int

class IssueStatusUpdate(BaseModel):
    status: StatusEnum

class IssueAssign(BaseModel):
    assignee_id: int