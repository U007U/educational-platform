from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Course, User
from .. import schemas


router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", response_model=schemas.CourseRead)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(
        title=course.title,
        description=course.description,
        teacher_id=course.teacher_id,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.get("/", response_model=List[schemas.CourseRead])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()
