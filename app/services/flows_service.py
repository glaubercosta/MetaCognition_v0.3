from typing import List, Optional
import json
from ..db import get_conn
from ..models import Flow, FlowCreate

def create_flow(data: FlowCreate) -> Flow:
    f = Flow(**data.model_dump())
    conn = get_conn(); cur = conn.cursor()
    cur.execute(
        "INSERT INTO flows (id,name,description,graph_json,created_at) VALUES (?,?,?,?,?)",
        (f.id, f.name, f.description, json.dumps(f.graph_json), f.created_at)
    )
    conn.commit(); conn.close()
    return f

def list_flows() -> List[Flow]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM flows ORDER BY created_at DESC")
    rows = cur.fetchall(); conn.close()
    out = []
    for r in rows:
        out.append(Flow(
            id=r["id"], name=r["name"], description=r["description"],
            graph_json=json.loads(r["graph_json"]) if r["graph_json"] else {},
            created_at=r["created_at"]
        ))
    return out

def get_flow(flow_id: str) -> Optional[Flow]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM flows WHERE id=?", (flow_id,))
    r = cur.fetchone(); conn.close()
    if not r: return None
    return Flow(
        id=r["id"], name=r["name"], description=r["description"],
        graph_json=json.loads(r["graph_json"]) if r["graph_json"] else {},
        created_at=r["created_at"]
    )
