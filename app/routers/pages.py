from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token") 

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/api/courses", response_class=HTMLResponse)
async def get_courses(request: Request, db: Session = Depends(get_db)):
    # Пока простой список
    return templates.TemplateResponse("courses.html", {"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, token: str = Depends(oauth2_scheme)):
    email = token.split('.')[1] if token else None  # JWT декод
    user_initial = email[0].upper() if email else '👤'
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user_email": email, 
        "user_initial": user_initial
    })

