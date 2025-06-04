from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.class_schema import ClassCreate, ClassOut, ClassUpdate
from app.crud import class_crud
from app.db.database import get_db

router = APIRouter(
    prefix="/classes",
    tags=["Clases"],
)

@router.post("/", response_model=ClassOut)
def create_new_class(class_data: ClassCreate, db: Session = Depends(get_db)):
    return class_crud.create_class(db=db, class_data=class_data)



@router.get("/read", response_model=list[ClassOut])
def read_all_classes(db: Session = Depends(get_db)):
    return class_crud.get_all_classes(db)


@router.get("/{class_id}", response_model=ClassOut)
def read_class_by_id(class_id: int, db: Session = Depends(get_db)):
    db_class = class_crud.get_class_by_id(db, class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class

@router.put("/{class_id}", response_model=ClassOut)
def update_existing_class(class_id: int, class_data: ClassUpdate, db: Session = Depends(get_db)):
    updated = class_crud.update_class(db, class_id, class_data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Class not found")
    return updated