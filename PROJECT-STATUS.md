# Project Status – EduPlatform

## Overview

EduPlatform is a learning platform project built to practice and demonstrate full‑stack development with FastAPI, PostgreSQL, Docker, Nginx, and a modern HTML/CSS UI.

This document is for personal/project planning: what is done, what is in progress, and what is planned next.

---

## Stack & Technologies

- **Backend**
  - FastAPI (Python)
  - Uvicorn for local development
  - Application structure:
    - `app/main.py` – application entrypoint, router mounting
    - `app/database.py` – database engine and session
    - `app/models.py` – database models
    - Routers in `app/routers/`:
      - `auth.py` – authentication
      - `users.py` – users
      - `courses.py` – courses
      - `lessons.py` – lessons
      - `pages.py` – HTML pages
      - `protected.py` – protected endpoints

- **Frontend**
  - Jinja2 templates
  - Component‑based CSS:
    - `static/css/components/cards.css` – shared card + icon components
    - Per‑page layout styles: `static/css/page/index.css`, `about.css`, `dashboard.css`, etc.

- **Database**
  - SQLite (`test.db`) for local development (temporary)
  - PostgreSQL planned for production

- **Infrastructure**
  - Docker / Docker Compose
    - `Dockerfile`
    - `docker-compose.yml`
  - Nginx as reverse proxy in front of FastAPI for production
    - `nginx.conf` prepared for future deployment [web:43][web:49]

- **Other**
  - Git, GitHub
  - Python virtual environments (venv)
  - Chart.js placeholder in dashboard for progress visualization [web:29]

---

## Implemented

### UI / Pages

- **Home page (`templates/page/index.html`)**
  - Hero section with CTA
  - “Why choose us” feature cards using shared `card` + `card-icon` components
  - Popular courses preview using `card card--course`
  - Call‑to‑action section

- **About page (`templates/page/about.html`)**
  - Hero text about the platform
  - Feature grid (FastAPI, PostgreSQL, Docker) using `card card--feature`
  - Stats section with key metrics
  - Team section using `card card--team` and shared icon styles

- **Dashboard (`templates/page/dashboard.html`)**
  - Welcome header with user email
  - Stats grid (Active courses, Completed lessons, Learning hours, Achievements)
    using unified `card card--feature` + `card-icon card-icon--feature`
  - Dashboard cards for:
    - My courses
    - Learning progress (Chart.js canvas placeholder)
    - Upcoming lessons (empty state)
    - News and updates

- **Courses page (`templates/page/courses.html`)**
  - Uses the same `courses-section` and `courses-grid` as the home page
  - Course cards built with `card card--course`, `card--course-image`, `card--course-body`
  - Consistent meta info: duration, level, and actions

- **Lessons page (`templates/page/lessons.html`)**
  - Reuses the course card component for lesson groups
  - Example lesson groups: Python basics, algorithms, web development

- **Auth pages**
  - `login.html` and `register.html` exist and are wired through the `auth` router (backend implementation present)

### CSS Architecture

- Introduced a shared **card component**:
  - `.card` – base card (background, border, radius, hover)
  - `.card-icon` – circular gradient icon container (same across all pages)
  - Modifiers:
    - `.card--feature`, `.card--team`, `.card--course`
    - `.card-icon--feature`, `.card-icon--team`
- Cleaned up per‑page CSS:
  - Page files handle only layout, grids, section spacing, and typography
  - Visual style of cards and icon circles is defined centrally in `cards.css`

### Backend

- FastAPI application with modular routers:
  - `auth` – login/registration logic (initial implementation)
  - `users` – user‑related endpoints
  - `courses` – course‑related endpoints
  - `lessons` – lesson‑related endpoints
  - `pages` – rendering HTML pages
  - `protected` – endpoints requiring authentication
- `database.py` and `models.py` provide the basis for working with a relational database (currently backed by `test.db` in development)

### DevOps / Repo

- Initial Docker and Nginx setup:
  - `Dockerfile` for building the app image
  - `docker-compose.yml` to orchestrate services
  - `nginx.conf` prepared as a reverse proxy configuration for FastAPI
- Git repository initialized with a clean structure:
  - `app/`, `templates/`, `static/`, `tests/`, `migrations/`
  - Status documentation in `PROJECT-STATUS.md`
  - Public project description in `README.md`

---

## In Progress

- Decide and finalize the ORM layer (SQLAlchemy vs SQLModel) and model structure
- Design and stabilize the database schema:
  - Users
  - Courses
  - Lessons
  - User progress / enrollments
- Prepare base API endpoints for:
  - Listing courses and lessons from the database
  - Providing dashboard data (stats, progress, upcoming lessons)

---

## Planned Next Steps

### Backend

- Implement authentication and authorization end‑to‑end:
  - Registration, login, logout flows
  - Session‑based or JWT‑based authentication
- Implement CRUD operations for:
  - Courses
  - Lessons
  - User progress
- Add full API documentation via FastAPI’s OpenAPI/Swagger UI

### Frontend

- Load courses and lessons dynamically from the backend (instead of static HTML)
- Implement filtering and search for courses and lessons
- Replace the dashboard placeholder with a real Chart.js‑based progress chart [web:29]

### DevOps / Deployment

- Connect PostgreSQL instead of SQLite for non‑test environments
- Configure Alembic (or similar) migrations in the `migrations/` folder
- Finalize Docker + Nginx deployment flow:
  - Nginx as reverse proxy to Uvicorn/Gunicorn [web:43][web:46]
  - Static file handling
  - HTTPS via Let’s Encrypt / Certbot (later)
- Add deployment documentation (Linux server + Docker + Nginx)

---

## Long‑Term Ideas

- Roles and permissions (student / instructor / admin)
- Course enrollment, certificates, and badges
- Comments / Q&A under lessons
- Multi‑language UI
