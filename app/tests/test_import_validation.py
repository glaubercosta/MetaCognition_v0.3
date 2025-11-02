from __future__ import annotations

import json

from fastapi.testclient import TestClient

from app.main import app
from app.models import Agent
client = TestClient(app)


def test_agent_prompt_limit(monkeypatch):
    monkeypatch.setenv("PROMPT_MAX_BYTES", "10")
    agent_payload = {
        "name": "Prompt Limited Agent",
        "role": "Test role",
        "prompt": "01234567890",  # 11 bytes
    }
    resp = client.post("/agents", json=agent_payload)
    assert resp.status_code == 422
    detail = resp.json()
    assert any("prompt exceeds the limit" in err["msg"] for err in detail["detail"])


def test_agent_prompt_boundary_accepts_limit(monkeypatch):
    monkeypatch.setenv("PROMPT_MAX_BYTES", "10")
    monkeypatch.setattr("app.routers.agents.svc.create_agent", lambda agent: Agent(**agent.model_dump()))
    agent_payload = {
        "name": "Prompt Boundary Agent",
        "role": "Test role",
        "prompt": "0123456789",  # exactly 10 bytes
    }
    resp = client.post("/agents", json=agent_payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["prompt"] == agent_payload["prompt"]


def test_agents_import_limit(monkeypatch):
    monkeypatch.setenv("IMPORT_MAX_ITEMS", "1")
    payload = [
        {"name": "Agent 1", "role": "R1", "prompt": "ok"},
        {"name": "Agent 2", "role": "R2", "prompt": "ok"},
    ]
    resp = client.post("/agents/import", json=payload)
    assert resp.status_code == 400
    data = resp.json()["detail"]
    assert data["ok"] is False
    assert "exceeds the limit" in data["message"]
    assert data["limit"] == 1
    assert data["count"] == 2


def test_agents_import_boundary_allows_limit(monkeypatch):
    monkeypatch.setenv("IMPORT_MAX_ITEMS", "2")
    monkeypatch.setattr("app.routers.agents_io.svc.create_agent", lambda agent: agent)
    payload = [
        {"name": "Agent 1", "role": "R1", "prompt": "ok"},
        {"name": "Agent 2", "role": "R2", "prompt": "ok"},
    ]
    resp = client.post("/agents/import", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] == 2
    assert [item["name"] for item in body["created"]] == ["Agent 1", "Agent 2"]


def test_agents_import_file_accepts_exact_limit(monkeypatch):
    payload = [
        {"name": "Agent 1", "role": "R1", "prompt": "ok"},
        {"name": "Agent 2", "role": "R2", "prompt": "ok"},
    ]
    data_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    limit = len(data_bytes)
    monkeypatch.setattr("app.routers.io_support.import_max_file_bytes", lambda: limit)
    monkeypatch.setattr("app.routers.io_support.import_max_items", lambda: 10)
    monkeypatch.setattr("app.routers.agents_io.svc.create_agent", lambda agent: agent)
    resp = client.post(
        "/agents/import",
        files={"file": ("agents.json", data_bytes, "application/json")},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] == 2


def test_agents_import_file_rejects_over_limit(monkeypatch):
    payload = [{"name": "Agent 1", "role": "R1", "prompt": "ok"}]
    data_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    monkeypatch.setattr("app.routers.io_support.import_max_file_bytes", lambda: len(data_bytes) - 1)
    monkeypatch.setattr("app.routers.io_support.import_max_items", lambda: 10)
    resp = client.post(
        "/agents/import",
        files={"file": ("agents.json", data_bytes, "application/json")},
    )
    assert resp.status_code == 413
    detail = resp.json()["detail"]
    assert detail["ok"] is False
    assert "Uploaded file exceeds" in detail["message"]
    assert "limit_bytes" in detail


def test_flow_validate_endpoint_returns_errors():
    payload = {"name": "", "graph_json": {"nodes": "invalid-type"}}
    resp = client.post("/flows/validate", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["ok"] is False
    assert any("name" in msg for msg in body["errors"])
    assert any("graph_json.nodes" in msg for msg in body["errors"])


def test_convert_agent_markdown_success(monkeypatch):
    monkeypatch.setenv("PROMPT_MAX_BYTES", "1000")
    markdown = """---
name: Markdown Agent
role: Summary helper
input_artifacts:
  input: ["file.md"]
output_artifacts:
  output: ["summary.txt"]
---
Use the provided context to generate a summary.
"""
    resp = client.post("/convert/agent-md", data=markdown, headers={"Content-Type": "text/markdown"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["ok"] is True
    agent = body["agent"]
    assert agent["name"] == "Markdown Agent"
    assert agent["prompt"].startswith("Use the provided context")


def test_convert_agent_markdown_invalid_yaml_returns_message():
    markdown = """---
name: Agent
items: [invalid
---
Body"""
    resp = client.post("/convert/agent-md", data=markdown, headers={"Content-Type": "text/markdown"})
    assert resp.status_code == 400
    detail = resp.json()["detail"]
    assert detail["ok"] is False
    assert "Invalid YAML front matter" in detail["message"]
    assert detail["errors"]


def test_flow_validate_success_message():
    payload = {"name": "Flow", "graph_json": {"nodes": [], "edges": []}}
    resp = client.post("/flows/validate", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["ok"] is True
    assert body["message"] == "Validation passed."
