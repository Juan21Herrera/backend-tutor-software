from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.db_users import User
from app.models.db_progress import StudentProgress
from app.routes.auth import get_current_user

router = APIRouter(
    prefix="/progress",
    tags=["Progreso"],
)

"""
Endpoint to get the progress of a user by their ID.
"""
@router.get("/{user_id}")
def get_progress(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if current_user.role == "student" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver el progreso de otro usuario")
    
    if user.role == "admin":
        if not user.group:
            raise HTTPException(status_code=400, detail="Administrador sin grupo asignado")
        
        students = db.query(User).filter(User.group == user.group, User.role == "student").all()
        if not students:
            return { "progress": 0.0 }
        
        students_ids = [s.id for s in students]
        avg = db.query(func.avg(StudentProgress.progress)).filter(StudentProgress.user_id.in_(students_ids)).scalar()
        return { "progress": round(avg or 0.0, 2) }
    
    raise HTTPException(status_code=400, detail="Rol no soportado")