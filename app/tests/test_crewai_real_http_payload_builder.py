import os
from fastapi.testclient import TestClient
from app.main import app
from app.integrations.crewai_client import CrewAIClient


def test_crewai_real_http_payload_contains_model_and_edges(monkeypatch):
    monkeypatch.setenv("CREWAI_MODE", "real")
    monkeypatch.setenv("CREWAI_API_KEY", "dummy")
    monkeypatch.setenv("CREWAI_HTTP_MODE", "http")
    monkeypatch.setenv("CREWAI_MODEL", "crewai-large")

    def fake_run_node(self, prompt: str, context=None):  # noqa: ANN001
        assert isinstance(prompt, str) and "node:" in prompt
        ctx = context or {}
        assert ctx.get("model") == os.getenv("CREWAI_MODEL")
        assert isinstance(ctx.get("edges"), list)
        assert ctx["metadata"]["flow"]["id"] == flow_id
        assert ctx["inputs"]["prompt"] == "P"
        return {"status": "ok", "output": f"ok-{ctx.get('node','?')}"}

    monkeypatch.setattr(CrewAIClient, "run_node", fake_run_node)

    client = TestClient(app)
    rf = client.post(
        "/flows",
        json={
            "name": "Payload Builder",
            "graph_json": {"nodes": [{"id": "a"}, {"id": "b"}], "edges": [{"from": "a", "to": "b"}]},
        },
    )
    assert rf.status_code == 201
    flow_id = rf.json()["id"]
    rr = client.post("/orchestrate/run", json={"engine": "crewai", "flow_id": flow_id, "inputs": {"prompt": "P"}})
    assert rr.status_code == 200
