Changelog
=========

All notable changes to this project are documented here.

Unreleased
----------

Added
- Fake engine adapter and contract tests:
  - `app/orchestration/engines/fake_adapter.py`
  - Router accepts `engine="fake"` in `app/routers/orchestrate.py`
  - Tests: `app/tests/test_engine_fake_contract.py`
- UI support for Fake engine and richer result display:
  - `frontend/src/pages/Orchestration.tsx` (adds Fake option and shows plan/logs)
  - `frontend/src/lib/api.ts` (engine type includes `"fake"`; flexible result shape)
- CI workflow with coverage:
  - `.github/workflows/ci.yml` (pytest with `--cov`)
  - `pytest-cov` added to `requirements.txt`
- Sprint 2 plan document:
  - `ManagementArtifacts/Documentacao/SPRINT_2_PLAN.md`
 - Multipart import endpoints + UI file upload:
   - API: `app/routers/agents_io.py`, `app/routers/flows_io.py` (UploadFile + Form)
   - UI: `frontend/src/lib/api.ts` (importAgentsFile/importFlowsFile), `frontend/src/pages/ImportExport.tsx`
 - CrewAI real adapter path with httpx client (feature flags):
   - Client: `app/integrations/crewai_client.py` (timeout/retries/backoff; response normalization)
   - Adapter: `app/orchestration/engines/crewai_real.py` (dry-run/http modes)

Changed
- API lifecycle migrated to FastAPI Lifespan; removed `@app.on_event`:
  - `app/main.py`
- Timestamps timezone-aware (UTC) for models:
  - `app/models.py` uses `datetime.now(datetime.UTC)`
- Router include order adjusted to avoid `/agents/{id}` collision with `/agents/export`:
  - `app/main.py`
- UI Orchestration page result rendering tolerates both `{plan, logs}` and `{result, duration_ms}`:
  - `frontend/src/pages/Orchestration.tsx`
 - Engines now publish `duration_ms` and structured JSON logs (ts, level, msg, node):
   - `app/orchestration/engines/fake_adapter.py`, `crewai_adapter.py`, `robotgreen_adapter.py`, `crewai_real.py`
- Branding/meta updates and minor docs:
  - `public/index.html` title/OG/Twitter
  - `README.md` adds local pytest with `PYTHONPATH` and coverage snippet
  - README envs for CrewAI flags (CREWAI_MODE, CREWAI_API_KEY, CREWAI_HTTP_MODE)
  - `ManagementArtifacts/Documentacao/ROADMAP.md` references Sprint 2 plan
  - `review_versao0.3-functional.md` aligned to Vite frontend
- Backlog updates (statuses and new items):
  - `ManagementArtifacts/Documentacao/JIRA_BACKLOG.csv`

Build
- Rebuilt frontend and deployed assets to `public/`.

v0.3.0 - 2025-10-12
-------------------

Added
- New React + Vite frontend integrated under `frontend/` (TypeScript + shadcn/ui).
- Makefile targets: `frontend-install`, `frontend-build`, `deploy-frontend`, `frontend-all`.
- Integration notes at `ProjectArtifacts/frontend_docs/INTEGRATION_NOTES.txt`.
- Git tag `ui-integration-v0.3` for safe rollback.

Changed
- FastAPI serves static UI from `public/` when present; fallback to `ui/public/`.
  See `app/main.py` mount logic.
- Dockerfile multi-stage build compiles frontend and copies assets to `/app/public/`.
- `.dockerignore` excludes `frontend/node_modules` and `frontend/dist` from context.

Security
- Executed `npm audit fix` and `npm audit fix --force` in `frontend/`.
- Upgraded Vite to v7; audit reports 0 vulnerabilities remaining.

Build
- Built frontend and deployed assets to `public/` for FastAPI to serve.
