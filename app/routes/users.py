from fastapi import APIRouter, Depends, HTTPException
from app.models.db_users import User as UserModel
from app.schemas.users import User, UserLogin, UserCreate
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models import db_users
from passlib.context import CryptContext
from app.routes.auth import create_access_token, verify_password, hash_password
from app.schemas.users import UserOut
from app.routes.auth import get_current_user
from app.models.db_progress import StudentProgress
from app.models.db_courses import Course
from app.schemas.users import StudentProfileResponse, TeacherProfileResponse
from app.schemas.users import UserProfileOut, CourseInfo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/user",
    tags=["Users"]   
)

# Get all users
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    data = db.query(db_users.User).all()
    return data

# Create a new user
@router.post("/register")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verify if the email already exists
    existing_user = db.query(db_users.User).filter(db_users.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    if user.role == "Estudiante" and not user.group:
        raise HTTPException(status_code=400, detail="Grupo es obligatorio para estudiantes.")
    # Create a new user
    new_user = UserModel (
        name=user.name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password),
        type_document=user.type_document,
        document=user.document,
        group=user.group,
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

# Login user
@router.post("/login")
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == user_login.email).first()

    if not user or not verify_password(user_login.password, user.password):
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

# Get User by ID
@router.post("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(db_users.User).filter(db_users.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Delete user by ID
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User delete successfully"}

# Update user by ID
@router.put("/{user_id}")
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.password = user.password
    db.commit()
    db.refresh(existing_user)
    return {"message": "User updated successfully"}

@router.get("/profile", response_model=StudentProfileResponse | TeacherProfileResponse)
def get_profile(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role.lower() == "estudiante":
        progress = db.query(StudentProgress).filter(StudentProgress.user_id == current_user.id).first()
        return {
            "role": "Estudiante",
            "profile": UserProfileOut(
                id=current_user.id,
                name=current_user.name,
                last_name=current_user.last_name,
                email=current_user.email,
                type_document=current_user.type_document,
                document=current_user.document,
                group=current_user.group,
                status=current_user.status,
                created_at=current_user.created_at,
            ),
            "progress": float(progress.progress) if progress else None,
            "comments": progress.comments if progress and progress.comments else None
        }
    elif current_user.role.lower() == "profesor":
        courses = db.query(Course).filter(Course.teacher_id == current_user.id).all()
        courses_summary = []
        for course in courses:
            students_count = db.query(UserModel).filter(UserModel.group == course.title, UserModel.role == "Estudiante").count()
            courses_summary.append(CourseInfo(
                id=course.id,
                title=course.title,
                students=None,  # O una lista si quieres incluir estudiantes
                students_count=students_count
            ))
        return {
            "role": "Profesor",
            "profile": UserProfileOut(
                id=current_user.id,
                name=current_user.name,
                last_name=current_user.last_name,
                email=current_user.email,
                type_document=current_user.type_document,
                document=current_user.document,
                group=current_user.group,
                status=current_user.status,
                created_at=current_user.created_at,
            ),
            "courses": courses_summary
        }
    raise HTTPException(status_code=400, detail="Invalid role")