.PHONY: up down test frontend-install frontend-build deploy-frontend frontend-all

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
deploy-frontend:
	mkdir -p public
	cp -r frontend/dist/* public/

# Install, build, and deploy in one go
frontend-all: frontend-install frontend-build deploy-frontend
