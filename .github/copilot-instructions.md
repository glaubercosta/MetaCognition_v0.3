# Copilot Instructions for MetaCognition_v0.3

## Project Overview
- **Purpose:** Orchestrates AI agents and flows via FastAPI, with adapters for multiple engines (CrewAI, RobotGreenAI), supporting import/export (JSON/YAML) and a React UI served by the API.
- **Stack:** Python 3.11, FastAPI, PyTest, SQLite, Docker, docker-compose.
- **Structure:**
  - `app/` — main backend logic
    - `routers/` — API endpoints (agents, flows, orchestration, evals)
    - `orchestration/engine.py` — engine selection logic
    - `orchestration/engines/` — adapters for external agent engines
    - `models.py`, `schemas.py` — ORM/data validation
    - `services/` — business logic for agents, flows, evals
    - `db.py` — SQLite setup
    - `tests/` — PyTest TDD tests
  - `ui/` — React UI (served statically, no build step)
  - `docker/` — Dockerfile for API
  - `docker-compose.yml` — multi-service orchestration

## Key Workflows
- **Run API & UI:**
  - `docker compose up --build` (serves API at `/docs`, UI at `/`)
- **Run Tests:**
  - `docker compose run --rm orchestrator pytest -q`
  - TDD: edit/add tests in `app/tests/`, follow Red→Green→Refactor
- **Import/Export:**
  - Agents/Flows: `GET/POST /agents/import|export`, `/flows/import|export` (accepts array or `{"items": [...]}`)
  - YAML import: send raw YAML string in body

## Patterns & Conventions
- **Adapters:** New agent engines integrate via `orchestration/engines/` and are selected in `engine.py`.
- **Service Layer:** Business logic in `services/`, API routes call these.
- **Data Models:** Use Pydantic schemas (`schemas.py`) and SQLAlchemy models (`models.py`).
- **Endpoints:** RESTful, grouped by resource (`agents`, `flows`, `orchestrate`, `evaluations`).
- **UI:** Static React app, no build required, served from `/ui/public`.
- **Config:** `.env` controls engine, log level, DB path. See `.env.example`.

## Integration Points
- **External Engines:** Adapters for CrewAI/RobotGreenAI (stubbed, extendable).
- **Database:** SQLite by default, path set in `.env`.
- **Static UI:** Served by FastAPI using `StaticFiles`.

## Examples
- Add new engine: create adapter in `orchestration/engines/`, update `engine.py`.
- Add new API route: create router in `routers/`, register in `main.py`.
- Add new test: create in `app/tests/`, run with PyTest via Docker.

---

**For AI agents:**
- Follow TDD: always add/modify tests in `app/tests/` before implementing features.
- Use service layer for business logic, keep routers thin.
- Prefer adapters for external integrations.
- Reference `.env.example` for config options.
- Use provided endpoints and data formats for import/export.

---

If any section is unclear or missing, please provide feedback for improvement.
