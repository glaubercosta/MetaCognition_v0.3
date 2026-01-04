import sqlite3, pathlib

DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "app.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS agents (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        goal TEXT NOT NULL,
        backstory TEXT NOT NULL,
        tools TEXT,
        input_artifacts TEXT,
        output_artifacts TEXT,
        created_at TEXT
    );
    """ )
    cur.execute("""
    CREATE TABLE IF NOT EXISTS flows (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        graph_json TEXT,
        created_at TEXT
    );
    """ )
    cur.execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
        id TEXT PRIMARY KEY,
        agent_id TEXT NOT NULL,
        score REAL NOT NULL,
        comments TEXT,
        created_at TEXT,
        FOREIGN KEY(agent_id) REFERENCES agents(id)
    );
    """ )
    conn.commit()
    conn.close()
