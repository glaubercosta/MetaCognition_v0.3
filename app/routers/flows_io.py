from fastapi import APIRouter, HTTPException, Body, UploadFile, File, Form, status, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from typing import Any, List
import yaml
from pydantic import ValidationError
from ..models import FlowCreate
from ..services import flows_service as svc
from .io_support import (
    read_payload_source,
    normalize_items,
    normalize_single,
    validation_errors_to_messages,
    build_error_detail,
)

router = APIRouter(prefix="/flows", tags=["flows-io"])

@router.get("/export")
def export_flows(format: str = "json"):
    flows = [f.model_dump() for f in svc.list_flows()]
    if format.lower() == "yaml":
        text = yaml.safe_dump(flows, sort_keys=False, allow_unicode=True)
        return PlainTextResponse(text, media_type="text/yaml")
    return JSONResponse(flows)

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
                detail=build_error_detail("Invalid JSON payload.", errors=[str(exc)]),
            ) from exc

    body = await request.body()
    if not body:
        return None
    try:
        return body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=build_error_detail("Request body must be UTF-8 encoded."),
        ) from exc


def _parse_flows_payload(
    payload: Any,
    fmt: str,
    file: UploadFile | None,
    file_format: str | None,
) -> List[FlowCreate]:
    raw = read_payload_source(payload, body_format=fmt, file=file, file_format=file_format)
    items = normalize_items(raw, context="flow")
    validated: List[FlowCreate] = []
    for idx, data in enumerate(items):
        try:
            validated.append(FlowCreate(**data))
        except ValidationError as exc:
            errors = validation_errors_to_messages(exc.errors())
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=build_error_detail(
                    f"Flow at index {idx} failed validation.",
                    errors=errors,
                    index=idx,
                ),
            ) from exc
    return validated


@router.post("/import")
async def import_flows(
    request: Request,
    payload: Any = Body(None),
    format: str = "json",
    file: UploadFile | None = File(default=None),
    file_format: str | None = Form(default=None),
):
    base_payload = await _ensure_payload_from_request(request, payload, file)
    flows = _parse_flows_payload(base_payload, format, file, file_format)
    created = [svc.create_flow(flow).model_dump() for flow in flows]
    return {"created": created, "count": len(created)}


@router.post("/validate")
def validate_flow_payload(payload: Any = Body(None), format: str = "json"):
    raw = read_payload_source(payload, body_format=format)
    data = normalize_single(raw, context="flow")
    try:
        FlowCreate(**data)
        return {"ok": True, "errors": [], "message": "Validation passed."}
    except ValidationError as exc:
        return {
            "ok": False,
            "errors": validation_errors_to_messages(exc.errors()),
            "message": "Validation failed.",
        }
