from __future__ import annotations

import re
from typing import Any, Dict

from fastapi import APIRouter, Body, HTTPException, status
import yaml
from pydantic import ValidationError

from ..models import AgentCreate
from .io_support import validation_errors_to_messages


router = APIRouter(prefix="/convert", tags=["convert"])


def _extract_front_matter(markdown: str) -> tuple[Dict[str, Any], str]:
    text = markdown.lstrip()
    pattern = r"^---\s*\n(.*?)\n---\s*\n?(.*)$"
    match = re.match(pattern, text, re.DOTALL)
    if not match:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={"message": "Markdown payload must start with a YAML front matter block."},
        )
    front_matter_raw, body = match.groups()
    try:
        data = yaml.safe_load(front_matter_raw) or {}
    except yaml.YAMLError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={"message": "Invalid YAML front matter.", "errors": [str(exc)]},
        ) from exc
    if not isinstance(data, dict):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={"message": "Front matter must define a mapping."},
        )
    return data, body.strip()


@router.post("/agent-md")
def convert_agent_markdown(markdown: str = Body(..., media_type="text/markdown")):
    if not isinstance(markdown, str) or not markdown.strip():
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={"message": "Markdown payload must be a non-empty string."},
        )

    meta, body = _extract_front_matter(markdown)
    agent_payload: Dict[str, Any] = {}
    allowed_fields = {"name", "role", "prompt", "input_artifacts", "output_artifacts"}
    for key, value in meta.items():
        if key in allowed_fields:
            agent_payload[key] = value

    prompt_text = agent_payload.get("prompt")
    if not prompt_text:
        agent_payload["prompt"] = body

    try:
        agent = AgentCreate(**agent_payload)
        return {"ok": True, "agent": agent.model_dump(), "errors": []}
    except ValidationError as exc:
        return {"ok": False, "errors": validation_errors_to_messages(exc.errors())}
