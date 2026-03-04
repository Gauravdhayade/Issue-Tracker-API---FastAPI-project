from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base
from sqlalchemy import Column, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(150), unique=True, index=True)
    password_hash = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    refresh_token = Column(String(500), nullable=True)