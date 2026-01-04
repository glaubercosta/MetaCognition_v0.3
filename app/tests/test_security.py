import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import AgentCreate

client = TestClient(app)

def test_html_sanitization():
    """Verify that HTML tags are stripped from agent input."""
    payload = {
        "name": "Hacker Agent",
        "role": "<b>Admin</b>",
        "prompt": "<script>alert('xss')</script>Do helpful things."
    }
    response = client.post("/agents", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["role"] == "Admin"
    assert data["prompt"] == "alert('xss')Do helpful things."
    assert "<" not in data["role"]
    assert "<" not in data["prompt"]

def test_rate_limiting():
    """Verify that rate limiting works (expect 429 after many requests)."""
    # Mock the remote address to ensure limiter works with TestClient
    from unittest.mock import patch
    with patch("slowapi.util.get_remote_address", return_value="127.0.0.1"):
        # Send enough requests to trigger the limit (100/minute)
        for _ in range(105):
            response = client.get("/health")
            if response.status_code == 429:
                break
        
        assert response.status_code == 429
