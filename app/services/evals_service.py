from typing import List
from ..db import get_conn
from ..models import Evaluation, EvaluationCreate

def create_evaluation(data: EvaluationCreate) -> Evaluation:
    e = Evaluation(**data.model_dump())
    conn = get_conn(); cur = conn.cursor()
    cur.execute(
        "INSERT INTO evaluations (id,agent_id,score,comments,created_at) VALUES (?,?,?,?,?)",
        (e.id, e.agent_id, e.score, e.comments, e.created_at)
    )
    conn.commit(); conn.close()
    return e

def list_evaluations() -> List[Evaluation]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM evaluations ORDER BY created_at DESC")
    rows = cur.fetchall(); conn.close()
    out = [Evaluation(
        id=r["id"], agent_id=r["agent_id"], score=r["score"], comments=r["comments"], created_at=r["created_at"]
    ) for r in rows]
    return out
