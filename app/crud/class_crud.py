from sqlalchemy.orm import Session
from app.models.db_class import Class
from app.schemas.class_schema import ClassCreate, ClassOut

def create_class(db: Session, class_data: ClassCreate):
    new_class = Class(**class_data.dict(), is_active=True)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

def get_all_classes(db: Session):
    return db.query(Class).filter(Class.is_active == True).all()

def get_class_by_id(db: Session, class_id: int):
    return db.query(Class).filter(Class.id == class_id, Class.is_active == True).first()

def update_class(db: Session, class_id: int, class_data: dict):
    db_class = db.query(Class).filter(Class.id == class_id, Class.is_active == True).first()
    if not db_class:
        return None
    print(f"Updating class {class_id} with data: {class_data}")
    for key, value in class_data.items():
        setattr(db_class, key, value)
    db.commit()
    db.refresh(db_class)
    return db_class