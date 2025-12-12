from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app import models


# Отдельная БД только для тестов (файл на диске, не мешает test.db из разработки)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tests.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Подменяем зависимость get_db на тестовую версию
app.dependency_overrides[get_db] = override_get_db

# Создаём таблицы в тестовой БД
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_db_setup_sanity():
    """
    Простой sanity‑тест: создаём пользователя и курс напрямую через ORM
    в тестовой БД, чтобы убедиться, что setup работает.
    """
    db = TestingSessionLocal()
    teacher = models.User(
        email="sanity@example.com",
        full_name="Sanity Teacher",
        hashed_password="dummy",
        role="teacher",
    )
    db.add(teacher)
    db.commit()
    db.refresh(teacher)

    course = models.Course(
        title="Sanity Course",
        description="Sanity check",
        teacher_id=teacher.id,
    )
    db.add(course)
    db.commit()
    db.refresh(course)

    db.close()

    # Проверяем, что приложение вообще живо с этой БД
    response = client.get("/")
    assert response.status_code == 200
