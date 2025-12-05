from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/protected", tags=["protected"])

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

async def get_current_user(token: str = Depends(lambda: "test"), db: Session = Depends(get_db)):
    """ВРЕМЕННАЯ ФУНКЦИЯ — токен пока не нужен"""
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="No users")
    return user

@router.get("/profile")
async def read_profile(current_user: User = Depends(get_current_user)):
    return {"user": current_user.email, "message": "Protected route works!"}

@router.get("/users")
async def protected_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": [{"email": u.email} for u in users]}
