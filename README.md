# EduPlatform

EduPlatform is a learning platform project built to practice and showcase full‑stack development with FastAPI, PostgreSQL, Docker, Nginx, and a custom HTML/CSS UI. [web:41]

## Overview

The project implements a simple educational portal with a home page, course and lesson listings, an “About” page, authentication pages, and a user dashboard.  
The focus is on a clean component‑based UI (shared cards and icon circles), a modular FastAPI backend, and a deployment‑ready structure using Docker and Nginx. [web:41][web:46]

## Tech Stack

- **Backend:** FastAPI (Python), Uvicorn  
- **Frontend:** Jinja2 templates, custom HTML + CSS  
- **UI Components:** Shared card and icon components (`static/css/components/cards.css`) reused across all pages  
- **Database:**
  - SQLite (`test.db`) for local development (via the default `DATABASE_URL` value)
  - PostgreSQL planned for production (configured via `DATABASE_URL` in `.env`)
- **ORM:** SQLAlchemy (classic `User`, `Course`, `Lesson` models in `app/models.py`)  
- **Deployment:**
  - Docker / Docker Compose (`Dockerfile`, `docker-compose.yml`)
  - Nginx as reverse proxy in front of FastAPI (`nginx.conf`) [web:43][web:49]

## Database configuration

- All ORM models are defined in `app/models.py` and inherit from a shared `Base` declared in `app/database.py`.  
- The database connection is configured via the `DATABASE_URL` environment variable; by default it falls back to `sqlite:///./test.db` for local development.  
- To switch to PostgreSQL, set `DATABASE_URL=postgresql+psycopg2://user:password@host:port/dbname` in `.env` and restart the application.

## Features

- Home page with hero section, feature cards, and popular courses  
- About page with platform description, stats, and team section  
- User dashboard with:
  - Stats cards (active courses, completed lessons, hours, achievements)
  - My courses, learning progress (Chart.js placeholder), upcoming lessons, news
- Courses page showing reusable course cards  
- Lessons page reusing the same course card component for lesson groups  
- Login and registration pages wired through the `auth` router  
- Single, consistent card and icon style across the whole application  

## Project Structure (UI & Backend)

- `app/main.py` – FastAPI app entrypoint and router registration  
- `app/database.py` – database engine and session configuration  
- `app/models.py` – database models  
- `app/routers/` – modular routers:
  - `auth.py`, `users.py`, `courses.py`, `lessons.py`, `pages.py`, `protected.py`

Templates:

- `templates/page/index.html` – Home  
- `templates/page/about.html` – About  
- `templates/page/dashboard.html` – Dashboard  
- `templates/page/courses.html` – Courses  
- `templates/page/lessons.html` – Lessons  
- `templates/page/login.html`, `templates/page/register.html` – auth pages  

CSS:

- `static/css/components/cards.css` – shared card + icon components  
- `static/css/page/index.css` – homepage sections and course grid  
- `static/css/page/about.css` – About page layout  
- `static/css/page/dashboard.css` – dashboard layout  

## Tests

- Basic testing is set up using `pytest` and `httpx` for the FastAPI application. [web:83]  
- A minimal smoke test in `tests/test_app_basic.py` verifies that the application starts and responds to HTTP requests.  
- Run tests with:

pytest

text

## Running Locally

Clone the repository:

git clone https://github.com/<your-username>/educational-platform.git
cd educational-platform

text

Create and activate virtual environment:

python -m venv venv

text

Linux / macOS:

source venv/bin/activate

text

Windows:

venv\Scripts\activate

text

Install dependencies:

pip install -r requirements.txt

text

Run the app:

uvicorn app.main:app --reload

text

Optionally, run tests to verify the setup:

pytest

text

The app will be available at `http://127.0.0.1:8000/`.

---

This project is under active development and is intended as both a learning playground and a portfolio example for FastAPI + PostgreSQL + Docker + Nginx. [web:41][web:46]