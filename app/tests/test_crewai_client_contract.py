import httpx
import pytest

from app.integrations.crewai_client import CrewAIClient


class _DummyResponse:
    def __init__(self, status_code: int, payload: dict):
        self.status_code = status_code
        self._payload = payload
        self.request = httpx.Request("POST", "https://dummy")

    def json(self) -> dict:
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("error", request=self.request, response=self)


def test_crewai_client_success(monkeypatch):
    recorded = {}

    class DummyClient:
        def __init__(self, *args, **kwargs):
            recorded["timeout"] = kwargs.get("timeout")

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def post(self, url, json=None, headers=None):
            recorded["url"] = url
            recorded["payload"] = json
            recorded["headers"] = headers
            return _DummyResponse(
                200,
                {
                    "status": "ok",
                    "results": [{"type": "text", "content": "crew-output"}],
                    "usage": {"prompt_tokens": 10, "completion_tokens": 5},
                },
            )

    monkeypatch.setattr(httpx, "Client", DummyClient)

    client = CrewAIClient(api_key="key-123", base_url="https://api.crewai.fake", timeout_sec=12, max_retries=0)
    resp = client.run_node(
        prompt="Generate summary",
        context={
            "node": "n42",
            "model": "crewai-large",
            "parameters": {"temperature": 0.2},
            "metadata": {"node": "n42", "flow": {"id": "flow-1", "name": "Main Flow", "size": 2}},
        },
    )

    assert resp["status"] == "ok"
    assert resp["output"] == "crew-output"
    assert resp["usage"] == {"prompt_tokens": 10, "completion_tokens": 5}
    assert recorded["headers"]["Authorization"] == "Bearer key-123"
    assert recorded["payload"]["metadata"]["flow"]["id"] == "flow-1"
    assert recorded["payload"]["parameters"]["temperature"] == 0.2
    assert recorded["timeout"] == 12


def test_crewai_client_error_payload(monkeypatch):
    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def post(self, url, json=None, headers=None):
            return _DummyResponse(200, {"status": "error", "error": {"message": "invalid prompt"}})

    monkeypatch.setattr(httpx, "Client", DummyClient)

    client = CrewAIClient(api_key="key-123", base_url="https://api.crewai.fake", max_retries=0)
    with pytest.raises(ValueError) as excinfo:
        client.run_node(prompt="bad", context={"node": "n1"})
    assert "invalid prompt" in str(excinfo.value)


def test_crewai_client_timeout_retries(monkeypatch):
    calls = {"count": 0}

    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def post(self, url, json=None, headers=None):
            calls["count"] += 1
            raise httpx.ReadTimeout("timeout", request=httpx.Request("POST", url))

    monkeypatch.setattr(httpx, "Client", DummyClient)
    monkeypatch.setattr("time.sleep", lambda *args, **kwargs: None)

    client = CrewAIClient(api_key="key-123", base_url="https://api.crewai.fake", max_retries=2, backoff_sec=0)
    with pytest.raises(httpx.ReadTimeout):
        client.run_node(prompt="timeout", context={"node": "n1"})
    assert calls["count"] == 3
