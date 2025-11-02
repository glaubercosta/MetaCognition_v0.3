.PHONY: up down test frontend-install frontend-build deploy-frontend frontend-all public-clean
.PHONY: frontend-windows

up:
	docker compose up --build

down:
	docker compose down -v

test:
	docker compose run --rm orchestrator pytest -q

# Install frontend dependencies
frontend-install:
	cd frontend && (npm ci || npm install)

# Build frontend with Vite
frontend-build:
	cd frontend && npm run build

# Copy built assets to public/ for FastAPI
deploy-frontend: public-clean
	mkdir -p public
	cp -r frontend/dist/* public/

# Install, build, and deploy in one go
frontend-all: frontend-install frontend-build deploy-frontend

public-clean:
	mkdir -p public/assets
	rm -rf public/assets/*

# Windows helper target: runs the PowerShell helper script which does install/build/copy
frontend-windows:
	@echo "Running Windows frontend helper (PowerShell)"
	@powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\frontend-build.ps1
