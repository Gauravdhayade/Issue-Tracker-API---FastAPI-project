from sqlalchemy import Column, Integer, ForeignKey, Enum
import enum
from app.core.database import Base

class RoleEnum(str, enum.Enum):
    Owner = "Owner"
    Admin = "Admin"
    Developer = "Developer"
    Viewer = "Viewer"

class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    role = Column(Enum(RoleEnum))