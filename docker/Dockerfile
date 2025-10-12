# 1) Build frontend (Vite) with Node in a separate stage
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
# Install dependencies
RUN npm ci || npm install
# Copy the rest of the frontend sources and build
COPY frontend/ ./
RUN npm run build

# 2) Backend image
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \ 
    build-essential curl ca-certificates sqlite3 \ 
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Copy built frontend assets into FastAPI public directory
RUN mkdir -p /app/public
COPY --from=frontend-builder /app/frontend/dist/ /app/public/
RUN mkdir -p /app/data

EXPOSE 8000
# Note: --reload is convenient for dev, but for production consider removing it.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
