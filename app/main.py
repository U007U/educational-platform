from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import os
from .database import engine, SessionLocal, Base, get_db
from .models import User, Course, Lesson

# Создаём таблицы (только один раз)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="🚀 Обучающая платформа", 
    description="FastAPI + PostgreSQL + Docker",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "🎓 Обучающая платформа готова!",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FastAPI"}

# Тестовая эндпоинт для БД (позже подключим PostgreSQL)
@app.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    return {"db": "connected", "tables": ["users", "courses", "lessons"]}
