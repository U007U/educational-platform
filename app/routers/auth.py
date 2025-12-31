from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.database import get_db
from app.models import User
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

templates = Jinja2Templates(directory="templates/page")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db)):
    """Получаем текущего пользователя из куков"""
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None
    
    user = db.query(User).filter(User.email == email).first()
    return user

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    user_email = request.cookies.get("user_email") or None
    return templates.TemplateResponse("register.html", {"request": request, "user_email": user_email})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user_email = request.cookies.get("user_email") or None
    return templates.TemplateResponse("login.html", {"request": request, "user_email": user_email})

@router.post("/register", response_model=Token)
def register(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """API регистрация (возвращает JSON Token)"""
    # Проверяем дубликат
    user = db.query(User).filter(User.email == form_data.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Создаём пользователя
    hashed_password = get_password_hash(form_data.password)
    db_user = User(
        email=form_data.username,
        full_name=form_data.username,
        hashed_password=hashed_password,
        role="student"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """API вход (возвращает JSON Token)"""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register-html", response_class=HTMLResponse)
async def register_html(request: Request, db: Session = Depends(get_db)):
    """HTML регистрация (возвращает HTML или редирект)"""
    form = await request.form()
    
    email = form.get("username")
    full_name = form.get("full_name")
    password = form.get("password")
    password_confirm = form.get("password_confirm")
    
    if password != password_confirm:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Пароли не совпадают!"})
    
    user = db.query(User).filter(User.email == email).first()
    if user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email уже зарегистрирован!"})
    
    hashed_password = get_password_hash(password)
    db_user = User(
        email=email,
        full_name=full_name or email,
        hashed_password=hashed_password,
        role="student"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Создаем токен для нового пользователя
    access_token = create_access_token(data={"sub": db_user.email})
    
    # Перенаправляем на dashboard с установкой куков
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800
    )
    response.set_cookie(
        key="user_email",
        value=db_user.email,
        max_age=1800
    )
    
    return response

@router.post("/login-html")
async def login_html(request: Request, db: Session = Depends(get_db)):
    """HTML вход (возвращает HTML или редирект)"""
    form = await request.form()
    
    email = form.get("username")
    password = form.get("password")
    
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "❌ Неверный email или пароль"
        })
    
    # Создаем токен и редиректим на dashboard
    access_token = create_access_token(data={"sub": user.email})
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800
    )
    response.set_cookie(
        key="user_email",
        value=user.email,
        max_age=1800
    )
    
    return response

@router.get("/logout")
async def logout():
    """Выход из системы"""
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="user_email")
    return response