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
    # Чистая БД для этого модуля
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def _register_and_get_token():
    form_data = {
        "username": "protected@example.com",
        "password": "secret123",
    }
    resp = client.post("/auth/register", data=form_data)
    assert resp.status_code == 200
    data = resp.json()
    return data["access_token"]


def test_protected_unauthorized():
    # Без токена должен быть 401
    resp = client.get("/protected/me")
    assert resp.status_code == 401
    body = resp.json()
    # Текст может чуть отличаться, главное — 401 и ошибка авторизации
    assert body["detail"] in ("Could not validate credentials", "Not authenticated")


def test_protected_authorized():
    token = _register_and_get_token()
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.get("/protected/me", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "protected@example.com"

def test_protected_invalid_token():
    # Явно некорректный JWT-токен (структура невалидна)
    invalid_token = "this.is.not.a.valid.jwt"

    resp = client.get(
        "/protected/me",
        headers={"Authorization": f"Bearer {invalid_token}"}
    )

    assert resp.status_code == 401
    body = resp.json()
    # Важно не «приковывать» себя к одной фразе, а описать класс проблемы
    assert body["detail"] in (
        "Could not validate credentials",
        "Not authenticated",
        "Invalid token or expired token",
    )

