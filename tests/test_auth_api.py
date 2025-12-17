from fastapi.testclient import TestClient
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.main import app  # noqa
from app.database import Base, engine  # noqa


client = TestClient(app)


def setup_module(module):
    # Для простоты: пересоздаём таблицы в тестовой БД, на которую мы уже сделали override.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_register_and_login():
    # 1. Регистрация
    form_data = {
        "username": "authuser@example.com",
        "password": "secret123",
    }
    response = client.post("/auth/register", data=form_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # 2. Логин теми же данными
    response = client.post("/auth/token", data=form_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_login_wrong_password():
    # Сначала регистрируем пользователя с корректным паролем
    register_data = {
        "username": "wrongpass@example.com",
        "password": "correct-password",
    }
    resp = client.post("/auth/register", data=register_data)
    assert resp.status_code == 200

    # Пытаемся залогиниться с тем же email, но другим (неверным) паролем
    login_data = {
        "username": "wrongpass@example.com",
        "password": "incorrect-password",
    }
    resp = client.post("/auth/token", data=login_data)

    assert resp.status_code == 401
    body = resp.json()
    # Текст может немного отличаться, фиксируем именно класс ошибки
    assert body["detail"] in (
        "Incorrect username or password",
        "Invalid credentials",
        "Could not validate credentials",
        "Incorrect credentials",
    )

def test_register_missing_password_returns_422():
    # Отправляем форму без обязательного поля password
    form_data = {
        "username": "no-password@example.com",
        # "password" намеренно не отправляем
    }

    resp = client.post("/auth/register", data=form_data)

    assert resp.status_code == 422
    body = resp.json()
    # FastAPI по умолчанию возвращает структуру ошибки в поле "detail"
    assert "detail" in body
    # Минимальная проверка: среди ошибок есть что-то про "password"
    # (это не жёсткий контракт, но даёт уверенность, что ошибка не какая‑то другая)
    assert any("password" in str(err.get("loc", [])) for err in body["detail"])

