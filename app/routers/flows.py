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
