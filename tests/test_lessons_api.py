from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Добавляем корень проекта в sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.main import app  # noqa
from app.database import Base, engine, SessionLocal  # noqa
from app import models  # noqa


client = TestClient(app)


def setup_module(module):
    """
    Для простоты пересоздаём все таблицы перед тестами этого модуля.
    Так мы начинаем тесты с чистой БД.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_lesson_for_course_and_get_by_course():
    # 1. Создаём преподавателя
    db = SessionLocal()
    teacher = models.User(
        email="lesson-teacher@example.com",
        full_name="Lesson Teacher",
        hashed_password="dummy-hash",
        role="teacher",
    )
    db.add(teacher)
    db.commit()
    db.refresh(teacher)

    # 2. Создаём курс для этого преподавателя
    course = models.Course(
        title="Lesson Course",
        description="Course for lessons",
        teacher_id=teacher.id,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    course_id = course.id
    db.close()

    # 3. Создаём урок через API
    lesson_payload = {
        "title": "First Lesson",
        "content": "Lesson content",
        "course_id": course_id,
    }

    response = client.post("/lessons/", json=lesson_payload)
    assert response.status_code == 200
    lesson_data = response.json()
    assert lesson_data["title"] == lesson_payload["title"]
    assert lesson_data["content"] == lesson_payload["content"]
    assert lesson_data["course_id"] == course_id

    # 4. Получаем все уроки
    response = client.get("/lessons/")
    assert response.status_code == 200
    lessons = response.json()
    assert len(lessons) == 1
    assert lessons[0]["title"] == lesson_payload["title"]

    # 5. Получаем уроки по course_id
    response = client.get(f"/lessons/course/{course_id}")
    assert response.status_code == 200
    course_lessons = response.json()
    assert len(course_lessons) == 1
    assert course_lessons[0]["course_id"] == course_id

def test_get_lessons_for_nonexistent_course_returns_404():
    nonexistent_course_id = 99999

    response = client.get(f"/lessons/course/{nonexistent_course_id}")

    # Главное требование контракта: ресурс не найден -> 404
    assert response.status_code == 404

    # Ответ не JSON, а HTML-страница 404, поэтому парсим как текст
    text = response.text
    # Минимально убеждаемся, что это именно страница об ошибке, а не что-то левое
    assert "404" in text or "Not Found" in text or "не найден" in text

def test_update_lesson_success():
    # создаём преподавателя и курс
    teacher_payload = {
        "email": "teacher-update@example.com",
        "full_name": "Teacher Update",
        "role": "teacher",
        "password": "secret123",
    }
    resp = client.post("/users/", json=teacher_payload)
    assert resp.status_code == 200
    teacher_id = resp.json()["id"]

    course_payload = {
        "title": "Course for lessons update",
        "description": "Desc",
        "teacher_id": teacher_id,
    }
    resp = client.post("/courses/", json=course_payload)
    assert resp.status_code == 200
    course_id = resp.json()["id"]

    # создаём урок
    lesson_payload = {
        "title": "Original lesson title",
        "content": "Original content",
        "course_id": course_id,
    }
    resp = client.post("/lessons/", json=lesson_payload)
    assert resp.status_code == 200
    lesson = resp.json()
    lesson_id = lesson["id"]

    # обновляем только title
    update_payload = {
        "title": "Updated lesson title",
    }
    resp = client.put(f"/lessons/{lesson_id}", json=update_payload)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["id"] == lesson_id
    assert updated["title"] == "Updated lesson title"
    assert updated["content"] == "Original content"

def test_update_nonexistent_lesson_returns_404():
    nonexistent_id = 99999
    update_payload = {
        "title": "Does not matter",
    }

    resp = client.put(f"/lessons/{nonexistent_id}", json=update_payload)

    assert resp.status_code == 404

    # Как и для курсов/пользователей, это HTML-страница 404
    text = resp.text
    assert "404" in text or "Not Found" in text or "не найден" in text


