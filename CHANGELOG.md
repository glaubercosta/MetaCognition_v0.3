Changelog
=========

All notable changes to this project are documented here.

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
