from fastapi import APIRouter, HTTPException
from typing import List
from ..models import Agent, AgentCreate
from ..services import agents_service as svc

router = APIRouter(prefix="/agents", tags=["agents"])

@router.post("", response_model=Agent, status_code=201)
def create_agent(agent: AgentCreate):
    return svc.create_agent(agent)

@router.get("", response_model=List[Agent])
def list_agents():
    return svc.list_agents()

@router.get("/{agent_id}", response_model=Agent)
def get_agent(agent_id: str):
    a = svc.get_agent(agent_id)
    if not a:
        raise HTTPException(404, "Agent not found")
    return a

@router.put("/{agent_id}", response_model=Agent)
def update_agent(agent_id: str, data: dict):
    a = svc.update_agent(agent_id, data)
    if not a:
        raise HTTPException(404, "Agent not found")
    return a

@router.delete("/{agent_id}", status_code=204)
def delete_agent(agent_id: str):
    ok = svc.delete_agent(agent_id)
    if not ok:
        raise HTTPException(404, "Agent not found")
    return
