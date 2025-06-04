from app.db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    teacher = relationship("User", back_populates="courses")
    Students = Column(Integer)