from fastapi import APIRouter, HTTPException, Body, UploadFile, File, Form
from fastapi.responses import PlainTextResponse, JSONResponse
from typing import Any
import yaml
from ..models import FlowCreate
from ..services import flows_service as svc

router = APIRouter(prefix="/flows", tags=["flows-io"])

@router.get("/export")
def export_flows(format: str = "json"):
    flows = [f.model_dump() for f in svc.list_flows()]
    if format.lower() == "yaml":
        text = yaml.safe_dump(flows, sort_keys=False, allow_unicode=True)
        return PlainTextResponse(text, media_type="text/yaml")
    return JSONResponse(flows)

@router.post("/import")
def import_flows(
    payload: Any = Body(None),
    format: str = "json",
    file: UploadFile | None = File(default=None),
    file_format: str | None = Form(default=None),
):
    try:
        # Multipart file upload takes precedence
        if file is not None:
            raw = file.file.read().decode("utf-8")
            use_fmt = (file_format or format or "json").lower()
            if use_fmt == "yaml":
                items = yaml.safe_load(raw) or []
            else:
                import json
                data = json.loads(raw)
                items = data.get("items", data) if isinstance(data, dict) else data
        elif isinstance(payload, str) and format.lower() == "yaml":
            items = yaml.safe_load(payload) or []
        elif isinstance(payload, list):
            items = payload
        elif isinstance(payload, dict) and "items" in payload:
            items = payload["items"]
        else:
            items = payload
        created = []
        for it in items:
            fc = FlowCreate(
                name=it.get("name", "Unnamed Flow"),
                description=it.get("description"),
                graph_json=it.get("graph_json") or {},
            )
            created.append(svc.create_flow(fc).model_dump())
        return {"created": created, "count": len(created)}
    except Exception as e:
        raise HTTPException(400, f"Import error: {e}")
