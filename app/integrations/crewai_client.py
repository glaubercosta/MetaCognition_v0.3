from __future__ import annotations

from typing import Any, Dict, Optional
import time
import httpx


class CrewAIClient:
    """
    Skeleton client for CrewAI integration.
    - Holds API key and base URL
    - Provides retry/timeout parameters
    - Exposes a simulate() path for CI/dev (no network)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.crewai.example",
        timeout_sec: int = 30,
        max_retries: int = 2,
        backoff_sec: float = 0.5,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.timeout_sec = timeout_sec
        self.max_retries = max_retries
        self.backoff_sec = backoff_sec

    def run_node(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Placeholder for a real HTTP call to CrewAI.
        Intentionally not implemented in this checkpoint to avoid network dependency.
        """
        ctx = context or {}
        payload = {"prompt": prompt, "context": ctx}
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                with httpx.Client(timeout=self.timeout_sec) as client:
                    resp = client.post(f"{self.base_url}/v1/run", json=payload, headers=headers)
                    if resp.status_code >= 500:
                        raise httpx.HTTPStatusError("server error", request=resp.request, response=resp)
                    resp.raise_for_status()
                    data = resp.json()
                    # Normalize possible response shapes into {status, output, error}
                    # 1) { status: 'ok'|'error', output?: str, error?: str }
                    if isinstance(data, dict) and ("status" in data or "output" in data or "error" in data):
                        status = data.get("status", "ok")
                        output = data.get("output")
                        error = data.get("error")
                        return {"status": status, "output": output, "error": error}
                    # 2) OpenAI-like: { choices: [ { message: { content }, text } ] }
                    if isinstance(data, dict) and "choices" in data:
                        try:
                            choices = data.get("choices") or []
                            first = choices[0] if choices else {}
                            content = (
                                (((first.get("message") or {}).get("content")) if isinstance(first, dict) else None)
                                or (first.get("text") if isinstance(first, dict) else None)
                            )
                            return {"status": "ok", "output": content, "error": None}
                        except Exception:
                            return {"status": "error", "output": None, "error": "invalid_response_shape"}
                    # 3) Unknown shape
                    return {"status": "error", "output": None, "error": "unknown_response_shape"}
            except Exception as e:  # httpx.RequestError | httpx.HTTPStatusError
                last_exc = e
                if attempt < self.max_retries:
                    time.sleep(self.backoff_sec * (attempt + 1))
                    continue
                raise

    def simulate(self, node_id: str, prompt_snippet: str) -> Dict[str, Any]:
        """Deterministic simulated response for CI/dev."""
        # Tiny delay to mimic processing without hurting CI speed
        time.sleep(0.01)
        return {
            "status": "ok",
            "output": f"crewai-real-{node_id}{('-' + prompt_snippet) if prompt_snippet else ''}",
        }
