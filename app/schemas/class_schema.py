from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ClassBase(BaseModel):
    title: str
    description: Optional[str] = None
    content_url: Optional[str] = None
    exercises: Optional[str] = None # JSON String
    exams: Optional[str] = None # JSON String
    recommendations: Optional[str] = None # JSON String

class ClassUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content_url: Optional[str] = None
    exercises: Optional[str] = None
    exams: Optional[str] = None
    recommendations: Optional[str] = None
    is_active: Optional[bool] = None

class ClassCreate(ClassBase):
    pass

class ClassOut(ClassBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    model_config = {
        "from_attributes": True
    }

