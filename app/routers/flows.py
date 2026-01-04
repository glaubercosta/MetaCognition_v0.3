from fastapi import APIRouter, HTTPException
from typing import List
from ..models import Flow, FlowCreate
from ..services import flows_service as svc

router = APIRouter(prefix="/flows", tags=["flows"])

@router.post("", response_model=Flow, status_code=201)
def create_flow(flow: FlowCreate):
    return svc.create_flow(flow)

@router.get("", response_model=List[Flow])
def list_flows():
    return svc.list_flows()

@router.get("/{flow_id}", response_model=Flow)
def get_flow(flow_id: str):
    f = svc.get_flow(flow_id)
    if not f:
        raise HTTPException(404, "Flow not found")
    return f

@router.put("/{flow_id}", response_model=Flow)
def update_flow(flow_id: str, flow: FlowCreate):
    # We use FlowCreate schema but treat fields as optional in service if needed, 
    # but Pydantic will enforce them. For partial updates we might need a different schema,
    # but for now let's assume full update or use dict(exclude_unset=True)
    updated = svc.update_flow(flow_id, flow.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(404, "Flow not found")
    return updated

@router.delete("/{flow_id}", status_code=204)
def delete_flow(flow_id: str):
    success = svc.delete_flow(flow_id)
    if not success:
        raise HTTPException(404, "Flow not found")
    return
