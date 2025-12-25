from app.database import get_db
from app.models import Course, Lesson


def create_lessons_for_course(db, course, lessons_data):
    existing = db.query(Lesson).filter(Lesson.course_id == course.id).count()
    if existing:
        print(f"- {course.title} (id={course.id}): уже есть {existing} уроков, пропускаем")
        return

    print(f"- {course.title} (id={course.id}): создаём {len(lessons_data)} уроков")

    for title, content in lessons_data:
        db.add(Lesson(title=title, content=content, course_id=course.id))


def main():
    db = next(get_db())
    courses = db.query(Course).all()
    print(f"Найдено курсов: {len(courses)}")

    # 1. Python for Beginners — оставить как есть (у тебя уже заполнен)
    beginners = next((c for c in courses if c.title == "Python for Beginners"), None)

    # 2. Backend на FastAPI
    backend = next((c for c in courses if c.title == "Python Backend"), None)
    if backend:
        backend.title = "Backend на FastAPI"
        backend.description = "Пишем простое backend‑приложение на FastAPI с БД и авторизацией."
        lessons_backend = [
            ("1. Введение в FastAPI", "Устанавливаем FastAPI и Uvicorn, разбираем базовый пример приложения."),
            ("2. Маршруты и запросы", "Создаём GET и POST эндпоинты, работаем с Path и Query параметрами."),
            ("3. Работа с базой данных", "Подключаем SQLAlchemy, добавляем модели и простые CRUD‑операции."),
            ("4. Аутентификация и токены", "Добавляем регистрацию и логин, защищаем маршруты JWT‑токеном."),
            ("5. Мини‑проект: API для заметок", "Собираем всё вместе: FastAPI + БД + авторизация для сервиса заметок."),
        ]
        create_lessons_for_course(db, backend, lessons_backend)

    # 3. Docker для разработчика
    docker = next((c for c in courses if c.title == "Docker DevOps"), None)
    if docker:
        docker.title = "Docker для разработчика"
        docker.description = "Учимся контейнеризировать приложения и поднимать окружение через docker‑compose."
        lessons_docker = [
            ("1. Зачем нужен Docker", "Понимаем, какие проблемы решают контейнеры и чем Docker лучше 'голой' системы."),
            ("2. Образы и контейнеры", "docker build, docker run, разбираем Dockerfile на простом Python‑примере."),
            ("3. Томы и сети", "Подключаем volume для данных и сети для общения сервисов между собой."),
            ("4. docker‑compose", "Определяем несколько сервисов (API + БД) в docker‑compose.yml."),
            ("5. Мини‑проект: контейнеризация FastAPI + Postgres", "Собираем приложение и БД в docker‑compose и запускаем единым командой."),
        ]
        create_lessons_for_course(db, docker, lessons_docker)

    # 4. Git и рабочий процесс
    git_course = next((c for c in courses if c.title == "Test Course 2"), None)
    if git_course:
        git_course.title = "Git и рабочий процесс"
        git_course.description = "Практический курс по Git: коммиты, ветки, pull‑request и работа с GitHub."
        lessons_git = [
            ("1. Основы Git", "Что такое репозиторий, индекс, коммит. Настраиваем Git и делаем первые коммиты."),
            ("2. Ветки и слияния", "Создаём ветки для задач, делаем merge, разрешаем конфликты."),
            ("3. Удалённые репозитории", "Подключаем GitHub, пушим и пуллим изменения."),
            ("4. Pull‑request и code review", "Создаём PR, комментируем изменения, обсуждаем правки."),
            ("5. Мини‑проект: учебный репозиторий", "Выполняем полный цикл: форк → ветка → изменения → PR → merge."),
        ]
        create_lessons_for_course(db, git_course, lessons_git)

    db.commit()
    db.close()
    print("✅ Обновление курсов и создание уроков завершено")


if __name__ == "__main__":
    main()
