from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models
from ..database import get_db
from ..models import Course, User, Lesson  # User сейчас не используется, но можно оставить
from .. import schemas

templates = Jinja2Templates(directory="templates/page")
router = APIRouter(
    prefix="/courses",
    tags=["courses"],
)


@router.post(
    "/",
    response_model=schemas.CourseRead,
    summary="Create course",
    description="Создаёт новый курс с заголовком, описанием и привязкой к преподавателю.",
)
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


@router.get(
    "/",
    response_model=List[schemas.CourseRead],
    summary="List of courses",
    description="Возвращает список всех доступных курсов.",
)
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()


@router.get(
    "/{course_id}",
    response_model=schemas.CourseRead,
    summary="Get course by ID",
    description="Возвращает данные курса по его идентификатору. Возвращает 404, если курс не найден.",
    responses={404: {"description": "Курс не найден"}},
)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    return course


@router.put(
    "/{course_id}",
    response_model=schemas.CourseRead,
    summary="Update course",
    description="Частично обновляет данные курса (например, заголовок и описание). Возвращает 404, если курс не найден.",
    responses={404: {"description": "Курс не найден"}},
)
def update_course(
    course_id: int,
    course_update: schemas.CourseUpdate,
    db: Session = Depends(get_db),
):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    update_data = course_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)

    db.commit()
    db.refresh(db_course)
    return db_course


@router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete course",
    description="Удаляет курс по ID. Возвращает 404, если курс не найден.",
    responses={404: {"description": "Курс не найден"}},
)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    db.delete(course)
    db.commit()
    # 204 No Content — тело не возвращаем
    return

@router.get("/course/{course_id}", response_class=HTMLResponse)
async def get_course_page(course_id: int, request: Request, db: Session = Depends(get_db)):
    course = db.execute(select(Course).filter(Course.id == course_id)).scalar_one_or_none()
    lessons = db.execute(select(Lesson).filter(Lesson.course_id == course_id)).scalars().all()
    
    print(f'🚀 COURSE #{course_id}: {course.title if course else "NOT FOUND"}')
    print(f'✅ LESSONS: {len(lessons)} уроки')
    
    if course:
        return templates.TemplateResponse("course_detail.html", {
            "request": request, 
            "course": course, 
            "lessons": lessons  # ← 5 уроков!
        })
    return templates.TemplateResponse("404.html", {"request": request})