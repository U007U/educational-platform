from fastapi.testclient import TestClient
import sys
from pathlib import Path

# 1. ЯВНО добавляем корень проекта в sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# 2. Теперь можно импортировать app.main
from app.main import app

client = TestClient(app)


def test_root_alive():
    response = client.get("/")
    assert response.status_code in (200, 404)

