from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
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


def test_agents_import_limit(monkeypatch):
    monkeypatch.setenv("IMPORT_MAX_ITEMS", "1")
    payload = [
        {"name": "Agent 1", "role": "R1", "prompt": "ok"},
        {"name": "Agent 2", "role": "R2", "prompt": "ok"},
    ]
    resp = client.post("/agents/import", json=payload)
    assert resp.status_code == 400
    data = resp.json()["detail"]
    assert data["limit"] == 1
    assert data["count"] == 2


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
