from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# =========================
# User schemas
# =========================

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "student"


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# Course schemas
# =========================

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None


class CourseCreate(CourseBase):
    teacher_id: int


class CourseRead(CourseBase):
    id: int
    teacher_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


# =========================
# Lesson schemas
# =========================

class LessonBase(BaseModel):
    title: str
    content: str


class LessonCreate(LessonBase):
    course_id: int


class LessonRead(LessonBase):
    id: int
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

    class Config:
        orm_mode = True
