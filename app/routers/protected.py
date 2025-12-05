from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import BaseModel
from typing import List
from app.database import get_db
from app.models import User, Course, Lesson

router = APIRouter(prefix="/protected", tags=["protected"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

class UserInfo(BaseModel):
    id: int
    email: str
    full_name: str
    role: str

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/profile", response_model=UserInfo)
def read_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/users/", response_model=List[UserInfo])
def protected_users(current_user: User = Depends(get_current_user)):
    return db.query(User).all()

@router.get("/courses/")
def protected_courses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Course).all()
