from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,autoincrement=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    type_document = Column(String, nullable=False)
    document = Column(Integer, unique=True, nullable=False)
    group = Column(String, nullable=True)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    status = Column(Boolean, default=True)
    progress = relationship("StudentProgress", back_populates="user", uselist=False)
    courses = relationship("Course", back_populates="teacher")