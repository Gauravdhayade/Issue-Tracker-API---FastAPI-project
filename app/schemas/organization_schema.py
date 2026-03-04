from pydantic import BaseModel
from datetime import datetime

class OrganizationCreate(BaseModel):
    name: str

class AddMember(BaseModel):
    user_id: int
    role: str

class OrganizationResponse(BaseModel):
    id: int
    name: str
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True