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

def test_get_nonexistent_course_returns_404():
    # Берём заведомо несуществующий id
    nonexistent_course_id = 99999

    response = client.get(f"/courses/{nonexistent_course_id}")

    assert response.status_code == 404
    # Ответ у тебя — HTML-страница 404, поэтому не парсим как JSON
    text = response.text
    # Минимальная проверка, что это действительно страница об ошибке 404
    assert "404" in text or "Not Found" in text or "не найден" in text

def test_create_course_missing_title_returns_422():
    # Создаём преподавателя, как в основном тесте
    db = SessionLocal()
    teacher = models.User(
        email="teacher-422@example.com",
        full_name="Teacher 422",
        hashed_password="dummy-hash",
        role="teacher",
    )
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    db.close()

    # Пытаемся создать курс БЕЗ title
    payload = {
        # "title": "Missing title",  # намеренно не отправляем
        "description": "Course without title",
        "teacher_id": teacher.id,
    }

    resp = client.post("/courses/", json=payload)

    assert resp.status_code == 422
    body = resp.json()
    assert "detail" in body
    # Убеждаемся, что среди ошибок фигурирует поле "title"
    assert any("title" in str(err.get("loc", [])) for err in body["detail"])

def test_delete_course_and_then_404_on_get():
    # 1. Готовим преподавателя
    db = SessionLocal()
    teacher = models.User(
        email="delete-teacher@example.com",
        full_name="Delete Teacher",
        hashed_password="dummy-hash",
        role="teacher",
    )
    db.add(teacher)
    db.commit()
    db.refresh(teacher)

    # 2. Создаём курс напрямую в БД
    course = models.Course(
        title="Course to delete",
        description="Will be deleted",
        teacher_id=teacher.id,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    course_id = course.id
    db.close()

    # 3. Удаляем курс через API
    resp = client.delete(f"/courses/{course_id}")
    # Пока допускаем оба варианта 200/204
    assert resp.status_code in (200, 204)

    # 4. Проверяем, что повторный GET даёт 404
    resp = client.get(f"/courses/{course_id}")
    assert resp.status_code == 404

def test_update_course_success():
    # создаём курс
    payload = {
        "title": "Original title",
        "description": "Original description",
        "teacher_id": 1,
    }
    resp = client.post("/courses/", json=payload)
    assert resp.status_code == 200
    course = resp.json()
    course_id = course["id"]

    # обновляем только title
    update_payload = {
        "title": "Updated title",
    }
    resp = client.put(f"/courses/{course_id}", json=update_payload)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["id"] == course_id
    assert updated["title"] == "Updated title"
    assert updated["description"] == "Original description"

def test_update_nonexistent_course_returns_404():
    nonexistent_id = 99999
    update_payload = {
        "title": "Does not matter",
    }

    resp = client.put(f"/courses/{nonexistent_id}", json=update_payload)

    assert resp.status_code == 404

    # Ответ — HTML-страница 404, не JSON
    text = resp.text
    assert "404" in text or "Not Found" in text or "не найден" in text


