from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime

class Class(Base):
    __tablename__="classes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    content_url = Column(String, nullable=True)
    exercises = Column(Text, nullable=True)
    exams = Column(Text, nullable=True)
    recommendations = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    is_active = Column(Boolean, default=True)