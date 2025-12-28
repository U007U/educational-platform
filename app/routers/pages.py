from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Course

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="templates/page")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user_email = request.cookies.get("user_email") or "Гость"
    return templates.TemplateResponse("index.html", {"request": request, "user_email": user_email})

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    print("🚀 ===== DASHBOARD (/dashboard) =======")
    user_email = request.cookies.get("user_email") or "Гость"
    return templates.TemplateResponse("dashboard.html", {"request": request, "user_email": user_email})

@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    user_email = request.cookies.get("user_email") or "Гость"
    return templates.TemplateResponse("about.html", {"request": request, "user_email": user_email})

@router.get("/courses", response_class=HTMLResponse)
async def courses_page(request: Request, db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    print(f'✅ COURSES: {len(courses)} курсов')
    return templates.TemplateResponse("courses.html", {"request": request, "courses": courses})

@router.get("/lessons", response_class=HTMLResponse)
async def lessons_page(request: Request):
    user_email = request.cookies.get("user_email") or "Гость"
    return templates.TemplateResponse("lessons.html", {"request": request, "user_email": user_email})

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    user_email = request.cookies.get("user_email") or None
    return templates.TemplateResponse("register.html", {"request": request, "user_email": user_email})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user_email = request.cookies.get("user_email") or None
    return templates.TemplateResponse("login.html", {"request": request, "user_email": user_email})

@router.get("/course/{course_id}", response_class=HTMLResponse)
async def get_course_page(course_id: int, request: Request, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course:
        return templates.TemplateResponse("course_detail.html", {
            "request": request, "course": course
        })
    return templates.TemplateResponse("404.html", {"request": request})
