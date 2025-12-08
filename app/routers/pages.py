from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import get_db
from sqlalchemy.orm import Session

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

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user_email = request.cookies.get("user_email") or "test@example.com"
    return templates.TemplateResponse("dashboard.html", {"request": request, "user_email": user_email})