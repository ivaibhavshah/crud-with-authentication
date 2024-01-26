from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=True)
    email = Column(String(100), nullable=True)
    password = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    is_deleted = Column(Boolean, default=False)
