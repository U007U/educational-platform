from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers import users, courses, lessons, auth, protected, pages

app = FastAPI(
    title="EduPlatform", 
    description="FastAPI + PostgreSQL + Docker",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/page")

app.include_router(pages.router, tags=["pages"])
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(lessons.router)
app.include_router(auth.router)
app.include_router(protected.router)

@app.exception_handler(404)
async def not_found(request: Request, exc):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FastAPI"}

@app.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    return {"db": "connected", "tables": ["users", "courses", "lessons"]}
