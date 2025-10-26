from __future__ import annotations

from typing import Any, Dict, Optional
import time
import httpx
import os


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
        # Allow runtime override of run path
        import os as _os
        self.run_path = _os.getenv("CREWAI_RUN_PATH", "/v1/run")

    def run_node(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Placeholder for a real HTTP call to CrewAI.
        Intentionally not implemented in this checkpoint to avoid network dependency.
        """
        ctx = context or {}
        model = ctx.get("model") or os.getenv("CREWAI_MODEL", "crewai-large")
        system_prompt = ctx.get("system_prompt") or "You are a helpful assistant."
        parameters = ctx.get("parameters") or {}
        messages = ctx.get("messages") or [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        metadata = ctx.get("metadata") or {}
        flow_meta = metadata.get("flow") if isinstance(metadata, dict) else None
        trimmed_ctx = {
            k: v
            for k, v in ctx.items()
            if k not in ("model", "system_prompt", "parameters", "messages", "metadata")
        }

        payload = {
            "model": model,
            "messages": messages,
            "parameters": parameters,
            "metadata": {
                "node": metadata.get("node") if isinstance(metadata, dict) else ctx.get("node"),
                "flow": {
                    "id": (flow_meta or {}).get("id"),
                    "name": (flow_meta or {}).get("name"),
                    "size": (flow_meta or {}).get("size"),
                },
                "extras": {
                    k: v
                    for k, v in (metadata.items() if isinstance(metadata, dict) else [])
                    if k != "flow"
                },
            },
        }
        if trimmed_ctx:
            payload["context"] = trimmed_ctx

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                with httpx.Client(timeout=self.timeout_sec) as client:
                    url = f"{self.base_url}{self.run_path}"
                    resp = client.post(url, json=payload, headers=headers)
                    if resp.status_code >= 500:
                        raise httpx.HTTPStatusError("server error", request=resp.request, response=resp)
                    resp.raise_for_status()
                    data = resp.json()
                    if not isinstance(data, dict):
                        return {"status": "error", "output": None, "error": "invalid_response_shape"}
                    status = data.get("status", "ok")
                    if status == "ok":
                        output = data.get("output")
                        if output is None and isinstance(data.get("results"), list):
                            first = data["results"][0] if data["results"] else {}
                            if isinstance(first, dict):
                                output = first.get("content") or first.get("text")
                        if output is None and isinstance(data.get("choices"), list):
                            first = data["choices"][0] if data["choices"] else {}
                            if isinstance(first, dict):
                                output = (
                                    (first.get("message") or {}).get("content")
                                    if isinstance(first.get("message"), dict)
                                    else None
                                ) or first.get("text")
                        return {
                            "status": "ok",
                            "output": output,
                            "error": None,
                            "usage": data.get("usage"),
                        }
                    if status == "error":
                        err = data.get("error")
                        if isinstance(err, dict):
                            message = err.get("message") or err.get("type") or "crew_error"
                        else:
                            message = err or "crew_error"
                        raise ValueError(message)
                    return {"status": status, "output": data.get("output"), "error": data.get("error")}
            except Exception as e:
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









