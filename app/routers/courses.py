from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from ...database import get_db
from ...models import Course, User

router = APIRouter(prefix="/courses", tags=["courses"])

class CourseCreate(BaseModel):
    title: str
    description: str
    teacher_id: int

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    teacher_id: int
    
    class Config:
        from_attributes = True

@router.post("/", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/", response_model=List[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()
