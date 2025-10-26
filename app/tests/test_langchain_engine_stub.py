from fastapi.testclient import TestClient

from app.main import app
from app import config as app_config


client = TestClient(app)


def test_langchain_engine_stub(monkeypatch):
    monkeypatch.setenv("LANGCHAIN_PROVIDER", "stub")
    monkeypatch.setenv("DEFAULT_ENGINE", "langchain")
    app_config.langchain_settings.cache_clear()

    agent_resp = client.post(
        "/agents",
        json={
            "name": "LangChain Stub Agent",
            "role": "Você atua como um assistente de teste.",
            "prompt": "Resuma os dados fornecidos.",
        },
    )
    assert agent_resp.status_code == 201
    agent_id = agent_resp.json()["id"]

    flow_resp = client.post(
        "/flows",
        json={
            "name": "LangChain Stub Flow",
            "graph_json": {
                "nodes": [{"id": "node-1", "agentId": agent_id}],
                "edges": [],
            },
        },
    )
    assert flow_resp.status_code == 201
    flow_id = flow_resp.json()["id"]

    run_resp = client.post(
        "/orchestrate/run",
        json={
            "flow_id": flow_id,
            "inputs": {"subject": "LangChain integration test"},
        },
    )
    assert run_resp.status_code == 200
    data = run_resp.json()
    assert data["engine"] == "langchain"
    artifacts = data["plan"]["artifacts"]
    assert "node-1" in artifacts
    assert artifacts["node-1"]["status"] == "ok"
    assert "langchain-stub" in artifacts["node-1"]["output"]
