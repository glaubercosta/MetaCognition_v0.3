from fastapi import APIRouter, HTTPException, Body, UploadFile, File, Form
from fastapi.responses import PlainTextResponse, JSONResponse
from typing import Any
import yaml
from ..models import AgentCreate
from ..services import agents_service as svc

router = APIRouter(prefix="/agents", tags=["agents-io"])

@router.get("/export")
def export_agents(format: str = "json"):
    agents = [a.model_dump() for a in svc.list_agents()]
    if format.lower() == "yaml":
        text = yaml.safe_dump(agents, sort_keys=False, allow_unicode=True)
        return PlainTextResponse(text, media_type="text/yaml")
    return JSONResponse(agents)

@router.post("/import")
def import_agents(
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
            ac = AgentCreate(
                name=it.get("name", "Unnamed Agent"),
                role=it.get("role"),
                prompt=it.get("prompt", ""),
                input_artifacts=it.get("input_artifacts"),
                output_artifacts=it.get("output_artifacts"),
            )
            created.append(svc.create_agent(ac).model_dump())
        return {"created": created, "count": len(created)}
    except Exception as e:
        raise HTTPException(400, f"Import error: {e}")
