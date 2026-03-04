from pydantic import BaseModel
from app.models.project import VisibilityEnum

class ProjectCreate(BaseModel):
    name: str
    project_key: str
    description: str
    visibility: VisibilityEnum