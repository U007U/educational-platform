from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
from .database import engine, SessionLocal, Base, get_db
from .models import User, Course, Lesson
from app.routers import users, courses, lessons, auth, protected, pages

# Создаём таблицы (только один раз)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EduPlatform", 
    description="FastAPI + PostgreSQL + Docker",
    version="1.0.0"
)

# ✅ STATIC FILES ПЕРВЫМИ (КРИТИЧНО!)
app.mount("/static", StaticFiles(directory="static"), name="static")

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
