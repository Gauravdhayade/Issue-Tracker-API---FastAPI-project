from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    issue_id = Column(Integer, ForeignKey("issues.id"))
    name = Column(String(50))