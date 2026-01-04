import sys, json
sys.path.insert(0, '/app')

from app.db import get_conn

def _loads(x): return json.loads(x) if x else None

conn = get_conn()
cur = conn.cursor()
cur.execute("SELECT * FROM agents ORDER BY created_at DESC LIMIT 1")
r = cur.fetchone()
conn.close()

print("Raw database row:")
print(f"  id: {r['id']}")
print(f"  name: {r['name']}")
print(f"  role: {r['role']}")
print(f"  goal: {r['goal'][:50]}...")
print(f"  backstory: {r['backstory'][:50]}...")
print(f"  tools (raw): {repr(r['tools'])}")
print(f"  tools (parsed): {_loads(r['tools'])}")
print(f"  tools (type): {type(_loads(r['tools']))}")

print("\nTrying to create Agent object...")
from app.models import Agent
try:
    agent = Agent(
        id=r["id"], name=r["name"], role=r["role"], goal=r["goal"], backstory=r["backstory"],
        tools=_loads(r["tools"]), input_artifacts=_loads(r["input_artifacts"]), 
        output_artifacts=_loads(r["output_artifacts"]), created_at=r["created_at"]
    )
    print(f"SUCCESS: Created agent {agent.name}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
