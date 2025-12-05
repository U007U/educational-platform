from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.database import get_db
from app.models import Lesson, Course

router = APIRouter(prefix="/lessons", tags=["lessons"])

class LessonCreate(BaseModel):
    title: str
    content: str
    course_id: int

class LessonResponse(BaseModel):
    id: int
    title: str
    content: str
    course_id: int
    
    class Config:
        from_attributes = True

@router.post("/", response_model=LessonResponse)
def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли курс
    course = db.query(Course).filter(Course.id == lesson.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_lesson = Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

@router.get("/", response_model=List[LessonResponse])
def get_lessons(db: Session = Depends(get_db)):
    return db.query(Lesson).all()

@router.get("/course/{course_id}", response_model=List[LessonResponse])
def get_lessons_by_course(course_id: int, db: Session = Depends(get_db)):
    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).all()
    if not lessons:
        raise HTTPException(status_code=404, detail="No lessons found for this course")
    return lessons
