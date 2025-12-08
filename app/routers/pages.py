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

# @router.get("/dashboard", response_class=HTMLResponse)
# async def dashboard(request: Request):
#     user_email = request.cookies.get("user_email") or "test@example.com"
#     print("🚀 ===== DASHBOARD РОУТ =======")
#     print(f"📧 user_email: '{request.cookies.get('user_email')}'")
    
#     try:
#         user_email = request.cookies.get("user_email")
#         print("✅ Template rendering...")
#         response = templates.TemplateResponse(
#             "page/dashboard.html",
#             {"request": request, "user_email": user_email}
#         )
#         print("✅ Template OK!")
#         return response
#     except Exception as e:
#         print(f"💥 ОШИБКА: {e}")
#         print(f"💥 TYPE: {type(e)}")
#         raise
#     return templates.TemplateResponse("page/dashboard.html", {"request": request, "user_email": user_email})
@router.get("/dashboard", response_class=HTMLResponse)
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

# В КОНЕЦ pages.py ДОБАВЬ:
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    user_email = request.cookies.get("user_email") or None
    return templates.TemplateResponse("register.html", {"request": request, "user_email": user_email})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user_email = request.cookies.get("user_email") or None
    return templates.TemplateResponse("login.html", {"request": request, "user_email": user_email})
