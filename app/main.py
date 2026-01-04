from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from contextlib import asynccontextmanager
from pathlib import Path
from .db import init_db
from .routers import agents, flows, orchestrate, evals, agents_io, flows_io, converters
from .middleware.security import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from .config import APP_ENV
from .utils.logging import setup_logging, request_id_ctx
import uuid

# Setup logging
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    logger.info("Application startup", extra={"app_env": APP_ENV})
    yield
    # Shutdown (no-op for now)


app = FastAPI(
    title="MetaCognition",
    version="0.3.0",
    lifespan=lifespan
)

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    token = request_id_ctx.set(request_id)
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
    finally:
        request_id_ctx.reset(token)

# from .config import APP_ENV # This line is moved up with other imports

# Security: Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

origins = ["*"]
if APP_ENV == "prod":
    origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health(request: Request):
    return {"status": "ok"}

# Register IO routes before dynamic ID routes to avoid collisions like /agents/export matching /agents/{id}
app.include_router(agents_io.router)
app.include_router(flows_io.router)
app.include_router(converters.router)
app.include_router(agents.router)
app.include_router(flows.router)
app.include_router(orchestrate.router)
app.include_router(evals.router)

# Serve UI static: prefer built React app in ./public if present; otherwise fallback to legacy ./ui/public
public_dir = "public"
legacy_ui_dir = os.path.join("ui", "public")
static_dir = public_dir if os.path.exists(os.path.join(public_dir, "index.html")) else legacy_ui_dir

app.mount("/", StaticFiles(directory=static_dir, html=True), name="ui")
