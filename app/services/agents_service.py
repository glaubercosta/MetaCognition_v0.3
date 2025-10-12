from typing import List, Optional, Dict, Any
import json
from ..db import get_conn
from ..models import Agent, AgentCreate

def _dumps(x): return json.dumps(x) if x is not None else None
def _loads(x): return json.loads(x) if x else None

def create_agent(data: AgentCreate) -> Agent:
    a = Agent(**data.model_dump())
    conn = get_conn(); cur = conn.cursor()
    cur.execute(
        "INSERT INTO agents (id,name,role,prompt,input_artifacts,output_artifacts,created_at) VALUES (?,?,?,?,?,?,?)",
        (a.id, a.name, a.role, a.prompt, _dumps(a.input_artifacts), _dumps(a.output_artifacts), a.created_at)
    )
    conn.commit(); conn.close()
    return a

def list_agents() -> List[Agent]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM agents ORDER BY created_at DESC")
    rows = cur.fetchall(); conn.close()
    out = []
    for r in rows:
        out.append(Agent(
            id=r["id"], name=r["name"], role=r["role"], prompt=r["prompt"],
            input_artifacts=_loads(r["input_artifacts"]), output_artifacts=_loads(r["output_artifacts"]),
            created_at=r["created_at"]
        ))
    return out

def get_agent(agent_id: str) -> Optional[Agent]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM agents WHERE id=?", (agent_id,))
    r = cur.fetchone(); conn.close()
    if not r: return None
    return Agent(
        id=r["id"], name=r["name"], role=r["role"], prompt=r["prompt"],
        input_artifacts=_loads(r["input_artifacts"]), output_artifacts=_loads(r["output_artifacts"]),
        created_at=r["created_at"]
    )

def update_agent(agent_id: str, data: Dict[str, Any]) -> Optional[Agent]:
    a = get_agent(agent_id)
    if not a: return None
    payload = a.model_dump(); payload.update(data)
    conn = get_conn(); cur = conn.cursor()
    cur.execute(
        "UPDATE agents SET name=?, role=?, prompt=?, input_artifacts=?, output_artifacts=? WHERE id=?",
        (payload["name"], payload.get("role"), payload.get("prompt",""),
         _dumps(payload.get("input_artifacts")), _dumps(payload.get("output_artifacts")), agent_id)
    )
    conn.commit(); conn.close()
    return get_agent(agent_id)

def delete_agent(agent_id: str) -> bool:
    conn = get_conn(); cur = conn.cursor()
    cur.execute("DELETE FROM agents WHERE id=?", (agent_id,))
    conn.commit(); deleted = cur.rowcount>0; conn.close()
    return deleted
