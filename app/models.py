from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid, datetime

class AgentCreate(BaseModel):
    name: str
    role: Optional[str] = None
    prompt: str = ""
    input_artifacts: Optional[Dict[str, Any]] = None
    output_artifacts: Optional[Dict[str, Any]] = None

class Agent(AgentCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

class FlowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    graph_json: Dict[str, Any]

class Flow(FlowCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

class EvaluationCreate(BaseModel):
    agent_id: str
    score: float
    comments: Optional[str] = None

class Evaluation(EvaluationCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
