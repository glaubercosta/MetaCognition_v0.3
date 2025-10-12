from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from .db import init_db
from .routers import agents, flows, orchestrate, evals
from .routers import agents_io, flows_io

app = FastAPI(title="Agent Orchestrator API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(agents.router)
app.include_router(flows.router)
app.include_router(orchestrate.router)
app.include_router(evals.router)
app.include_router(agents_io.router)
app.include_router(flows_io.router)

# Serve UI static: prefer built React app in ./public if present; otherwise fallback to legacy ./ui/public
public_dir = "public"
legacy_ui_dir = os.path.join("ui", "public")
static_dir = public_dir if os.path.exists(os.path.join(public_dir, "index.html")) else legacy_ui_dir

app.mount("/", StaticFiles(directory=static_dir, html=True), name="ui")
