from fastapi import APIRouter, HTTPException, Body, UploadFile, File, Form, status, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from typing import Any, List
import yaml
from pydantic import ValidationError
from ..models import AgentCreate
from ..services import agents_service as svc
from .io_support import (
    read_payload_source,
    normalize_items,
    normalize_single,
    validation_errors_to_messages,
)

router = APIRouter(prefix="/agents", tags=["agents-io"])

@router.get("/export")
def export_agents(format: str = "json"):
    agents = [a.model_dump() for a in svc.list_agents()]
    if format.lower() == "yaml":
        text = yaml.safe_dump(agents, sort_keys=False, allow_unicode=True)
        return PlainTextResponse(text, media_type="text/yaml")
    return JSONResponse(agents)

async def _ensure_payload_from_request(request: Request, payload: Any, file: UploadFile | None) -> Any:
    if payload is not None or file is not None:
        return payload

    content_type = (request.headers.get("content-type") or "").split(";")[0].strip().lower()
    if content_type == "application/json":
        try:
            return await request.json()
        except Exception as exc:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail={"message": "Invalid JSON payload.", "errors": [str(exc)]},
            ) from exc

    body = await request.body()
    if not body:
        return None
    try:
        return body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={"message": "Request body must be UTF-8 encoded."},
        ) from exc


def _parse_agents_payload(
    payload: Any,
    fmt: str,
    file: UploadFile | None,
    file_format: str | None,
) -> List[AgentCreate]:
    raw = read_payload_source(payload, body_format=fmt, file=file, file_format=file_format)
    items = normalize_items(raw, context="agent")
    validated: List[AgentCreate] = []
    for idx, data in enumerate(items):
        try:
            validated.append(AgentCreate(**data))
        except ValidationError as exc:
            errors = validation_errors_to_messages(exc.errors())
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": f"Agent at index {idx} failed validation.",
                    "errors": errors,
                    "index": idx,
                },
            ) from exc
    return validated


@router.post("/import")
async def import_agents(
    request: Request,
    payload: Any = Body(None),
    format: str = "json",
    file: UploadFile | None = File(default=None),
    file_format: str | None = Form(default=None),
):
    base_payload = await _ensure_payload_from_request(request, payload, file)
    agents = _parse_agents_payload(base_payload, format, file, file_format)
    created = [svc.create_agent(agent).model_dump() for agent in agents]
    return {"created": created, "count": len(created)}


@router.post("/validate")
def validate_agent_payload(payload: Any = Body(None), format: str = "json"):
    raw = read_payload_source(payload, body_format=format)
    data = normalize_single(raw, context="agent")
    try:
        AgentCreate(**data)
        return {"ok": True, "errors": []}
    except ValidationError as exc:
        return {"ok": False, "errors": validation_errors_to_messages(exc.errors())}
