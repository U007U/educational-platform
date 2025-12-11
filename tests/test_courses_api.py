from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Добавляем корень проекта в sys.path (как в test_app_basic.py)
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.main import app  # noqa
from app.database import Base, engine, SessionLocal  # noqa
from app import models  # noqa


client = TestClient(app)


def setup_module(module):
    """
    Простой setup для учебного проекта:
    - пересоздаём таблицы перед тестами,
    - работаем с той же SQLite-базой.
    В будущем это можно заменить на отдельную тестовую БД.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_and_list_courses():
    # 1. Создаём курс через API
    payload = {
        "title": "Test Course",
        "description": "Test description",
        "teacher_id": 1,
    }

    # Чтобы teacher_id=1 существовал, создадим такого пользователя напрямую в БД
    db = SessionLocal()
    teacher = models.User(
        email="teacher@example.com",
        full_name="Test Teacher",
        hashed_password="dummy-hash",
        role="teacher",
    )
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    db.close()

    # Обновляем payload с реальным teacher_id
    payload["teacher_id"] = teacher.id

    response = client.post("/courses/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["teacher_id"] == payload["teacher_id"]

    # 2. Получаем список курсов и проверяем, что курс там есть
    response = client.get("/courses/")
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) == 1
    assert courses[0]["title"] == payload["title"]
