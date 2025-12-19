from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Добавляем корень проекта в sys.path (как в других тестах)
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.main import app  # noqa
from app.database import Base, engine  # noqa


client = TestClient(app)


def setup_module(module):
    """
    Простой setup: пересоздаём таблицы перед тестами этого модуля.
    Для учебного проекта этого достаточно.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_and_get_user():
    payload = {
        "email": "user@example.com",
        "full_name": "Test User",
        "role": "student",
        "password": "secret123",
    }

    # 1. Создаём пользователя
    response = client.post("/users/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert data["role"] == payload["role"]
    assert "id" in data
    assert "created_at" in data
    user_id = data["id"]

        # 2. Получаем список пользователей
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()

    # В списке может быть больше пользователей (добавлены другими тестами),
    # поэтому проверяем, что среди них есть наш user_id.
    ids = [u["id"] for u in users]
    assert user_id in ids


    # 3. Получаем пользователя по id
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == payload["email"]

def test_get_nonexistent_user_returns_404():
    # Берём заведомо несуществующий id
    nonexistent_user_id = 99999

    resp = client.get(f"/users/{nonexistent_user_id}")

    # Главное: ресурс не найден -> 404
    assert resp.status_code == 404

    # Ответ — HTML-страница 404, поэтому не парсим как JSON
    text = resp.text
    # Минимальная проверка, что это действительно страница об ошибке
    assert "404" in text or "Not Found" in text or "не найден" in text
