# models/progress.py
from app.db.database import Base
from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship

class StudentProgress(Base):
    __tablename__ = "student_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    progress = Column(String, nullable=False)
    comments = Column(String, nullable=True)
    user = relationship("User", back_populates="progress")