from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

# Serve UI static (React CDN)
app.mount("/", StaticFiles(directory="ui/public", html=True), name="ui")
