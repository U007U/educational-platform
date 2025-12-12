from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Lesson, Course
from app import schemas


router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.post("/", response_model=schemas.LessonRead)
def create_lesson(lesson: schemas.LessonCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли курс
    course = db.query(Course).filter(Course.id == lesson.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    db_lesson = Lesson(
        title=lesson.title,
        content=lesson.content,
        course_id=lesson.course_id,
    )
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


@router.get("/", response_model=List[schemas.LessonRead])
def get_lessons(db: Session = Depends(get_db)):
    return db.query(Lesson).all()


@router.get("/course/{course_id}", response_model=List[schemas.LessonRead])
def get_lessons_by_course(course_id: int, db: Session = Depends(get_db)):
    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).all()
    if not lessons:
        raise HTTPException(status_code=404, detail="No lessons found for this course")
    return lessons
