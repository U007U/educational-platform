from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# Удалите точку перед database и models:
from app.database import engine, Base, get_db
from app.models import User, Course, Lesson
from app.routers import users, courses, lessons, auth, protected, pages

# Остальной код оставьте без изменений

# Создаём таблицы (только один раз)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EduPlatform", 
    description="FastAPI + PostgreSQL + Docker",
    version="1.0.0"
)

# ✅ STATIC FILES ПЕРВЫМИ (КРИТИЧНО!)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ ШАБЛОНЫ
templates = Jinja2Templates(directory="templates/page")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    user_email = request.cookies.get("user_email") or "test@example.com"
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user_email": user_email}
    )

# @app.get("/dashboard", response_class=HTMLResponse)
# async def dashboard(request: Request):
#     user_email = request.cookies.get("user_email")
#     if not user_email:
#         return RedirectResponse(url="/login")
    
#     return templates.TemplateResponse(
#         "dashboard.html",
#         {"request": request, "user_email": user_email}
#     )
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    print("🔥 MAIN DASHBOARD HIT!")  # ← ДОБАВЬ
    user_email = request.cookies.get("user_email") or "test@example.com"
    return templates.TemplateResponse("dashboard.html", {"request": request, "user_email": user_email})

@app.get("/docs", response_class=HTMLResponse)
async def api_docs(request: Request):
    user_email = request.cookies.get("user_email") or "test@example.com"
    return templates.TemplateResponse(
        "docs.html",
        {"request": request, "user_email": user_email}
    )

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    user_email = request.cookies.get("user_email") or "test@example.com"
    return templates.TemplateResponse(
        "about.html",
        {"request": request, "user_email": user_email}
    )


# 404 страница
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return templates.TemplateResponse(
        "404.html",
        {"request": request},
        status_code=404
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FastAPI"}

@app.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    return {"db": "connected", "tables": ["users", "courses", "lessons"]}

# Роутеры ПОСЛЕ StaticFiles
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(lessons.router)
app.include_router(auth.router)
app.include_router(protected.router)
app.include_router(pages.router)

security_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    auto_error=False
)
