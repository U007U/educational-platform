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
