from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
import uuid, datetime

from .config import prompt_max_bytes


class AgentCreate(BaseModel):
    name: str
    role: Optional[str] = None
    prompt: str
    input_artifacts: Optional[Dict[str, Any]] = None
    output_artifacts: Optional[Dict[str, Any]] = None

    @field_validator("name")
    @classmethod
    def _validate_name(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("name must be a non-empty string.")
        return value.strip()

    @field_validator("prompt")
    @classmethod
    def _validate_prompt(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("prompt must be a string.")
        limit = prompt_max_bytes()
        if limit > 0 and len(value.encode("utf-8")) > limit:
            raise ValueError(f"prompt exceeds the limit of {limit} bytes.")
        return value

class Agent(AgentCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).isoformat())

class FlowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    graph_json: Dict[str, Any]

    @field_validator("name")
    @classmethod
    def _validate_name(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("name must be a non-empty string.")
        return value.strip()

    @field_validator("graph_json")
    @classmethod
    def _validate_graph_json(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(value, dict):
            raise ValueError("graph_json must be a JSON object.")
        nodes = value.get("nodes")
        if nodes is not None and not isinstance(nodes, list):
            raise ValueError("graph_json.nodes must be a list when provided.")
        edges = value.get("edges")
        if edges is not None and not isinstance(edges, list):
            raise ValueError("graph_json.edges must be a list when provided.")
        return value

class Flow(FlowCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).isoformat())

class EvaluationCreate(BaseModel):
    agent_id: str
    score: float
    comments: Optional[str] = None

class Evaluation(EvaluationCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).isoformat())
