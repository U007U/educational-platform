from urllib import request
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from app.database import get_db
from sqlalchemy.orm import Session

from app.models import Course, Lesson

router = APIRouter()
templates = Jinja2Templates(directory="templates/page")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user_email = request.cookies.get("user_email") or "test@example.com"
    return templates.TemplateResponse("index.html", {"request": request, "user_email": user_email})

@router.get("/api/courses", response_class=HTMLResponse)
async def get_courses(request: Request, db: Session = Depends(get_db)):
    # Пока простой список
    return templates.TemplateResponse("courses.html", {"request": request})

async def dashboard(request: Request):
    print("🚀 ===== PAGES DASHBOARD РОУТ (/pages/dashboard) =======")
    user_email = request.cookies.get("user_email") or "test@example.com"
    print(f"📧 user_email: '{user_email}'")
    
    try:
        print("✅ Rendering dashboard.html...")
        response = templates.TemplateResponse(
            "dashboard.html",  # ✅ БЕЗ "page/"
            {"request": request, "user_email": user_email}
        )
        print("✅ PAGES DASHBOARD OK!")
        return response
    except Exception as e:
        print(f"💥 PAGES DASHBOARD ERROR: {e}")
        raise
   

@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    user_email = request.cookies.get("user_email") or "test@example.com"
    return templates.TemplateResponse(
        "page/about.html",
        {"request": request, "user_email": user_email}
    )

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    user_email = request.cookies.get("user_email") or None
    return templates.TemplateResponse("register.html", {"request": request, "user_email": user_email})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user_email = request.cookies.get("user_email") or None
    return templates.TemplateResponse("login.html", {"request": request, "user_email": user_email})

@router.get("/courses", response_class=HTMLResponse)
async def courses_page(request: Request, db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    print(f'✅ COURSES ROUTE: {len(courses)} courses!')
    print(f'✅ TITLES: {[c.title for c in courses]}')
    return templates.TemplateResponse("courses.html", {"request": request, "courses": courses})


@router.get("/course/{course_id}", response_class=HTMLResponse)
async def get_course_page(course_id: int, request: Request, db: Session = Depends(get_db)):
    course = db.execute(select(Course).filter(Course.id == course_id)).scalar_one_or_none()
    lessons = db.execute(select(Lesson).filter(Lesson.course_id == course_id)).scalars().all()
    
    print(f'🚀 PAGES COURSE #{course_id}: {course.title if course else "NOT FOUND"}')
    print(f'✅ LESSONS: {len(lessons)} уроки')
    
    if course:
        return templates.TemplateResponse("course_detail.html", {
            "request": request, 
            "course": course, 
            "lessons": lessons
        })
    return templates.TemplateResponse("404.html", {"request": request})

