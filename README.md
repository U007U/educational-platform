# EduPlatform

EduPlatform is a learning platform project built to practice and showcase full‑stack development with FastAPI, PostgreSQL, Docker, Nginx, and a custom HTML/CSS UI.

## Overview

The project implements a simple educational portal with a home page, course and lesson listings, an “About” page, authentication pages, and a user dashboard.  
The focus is on a clean component‑based UI (shared cards and icon circles), a modular FastAPI backend, and a deployment‑ready structure using Docker and Nginx.

## Tech Stack

- **Backend:** FastAPI (Python), Uvicorn
- **Frontend:** Jinja2 templates, custom HTML + CSS
- **UI Components:** Shared card and icon components (`static/css/components/cards.css`) reused across all pages
- **Database:**
  - SQLite (`test.db`) for local development
  - PostgreSQL planned for production
- **ORM:** SQLAlchemy or SQLModel (to be finalized)
- **Deployment:**
  - Docker / Docker Compose (`Dockerfile`, `docker-compose.yml`)
  - Nginx as reverse proxy in front of FastAPI (`nginx.conf`) [web:43][web:49]

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

## Running Locally

Clone the repository
git clone https://github.com/<your-username>/educational-platform.git
cd educational-platform

Create and activate virtual environment
python -m venv venv

Linux / macOS
source venv/bin/activate

Windows
venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Run the app
uvicorn app.main:app --reload

text

The app will be available at `http://127.0.0.1:8000/`.

---

This project is under active development and is intended as both a learning playground and a portfolio example for FastAPI + PostgreSQL + Docker + Nginx. [web:41][web:46]