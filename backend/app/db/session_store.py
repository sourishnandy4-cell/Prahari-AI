"""
Session & Conversation persistence layer using SQLite (air-gapped, no external DB).

Schema:
  sessions(id TEXT PK, title TEXT, created_at TEXT, updated_at TEXT)
  messages(id TEXT PK, session_id TEXT FK, role TEXT, content TEXT, citations TEXT, metadata TEXT, created_at TEXT)
"""
import sqlite3
import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

from backend.app.config import settings


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def _get_conn():
    conn = sqlite3.connect(settings.SESSION_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    """Create tables if they don't exist. Called once at app startup."""
    with _get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id         TEXT PRIMARY KEY,
                title      TEXT NOT NULL DEFAULT 'New Session',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS messages (
                id         TEXT PRIMARY KEY,
                session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                role       TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                content    TEXT NOT NULL,
                citations  TEXT,
                metadata   TEXT,
                created_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id, created_at);
        """)


# ── Sessions ───────────────────────────────────────────────────────────────────

def create_session(title: Optional[str] = None) -> Dict[str, Any]:
    sid = str(uuid.uuid4())
    now = _now()
    title = title or "New Session"
    with _get_conn() as conn:
        conn.execute(
            "INSERT INTO sessions(id, title, created_at, updated_at) VALUES (?,?,?,?)",
            (sid, title, now, now)
        )
    return {"id": sid, "title": title, "created_at": now, "updated_at": now}


def list_sessions() -> List[Dict[str, Any]]:
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM sessions ORDER BY updated_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM sessions WHERE id=?", (session_id,)
        ).fetchone()
    return dict(row) if row else None


def rename_session(session_id: str, title: str) -> bool:
    with _get_conn() as conn:
        cur = conn.execute(
            "UPDATE sessions SET title=?, updated_at=? WHERE id=?",
            (title, _now(), session_id)
        )
    return cur.rowcount > 0


def delete_session(session_id: str) -> bool:
    with _get_conn() as conn:
        cur = conn.execute("DELETE FROM sessions WHERE id=?", (session_id,))
    return cur.rowcount > 0


# ── Messages ───────────────────────────────────────────────────────────────────

def add_message(
    session_id: str,
    role: str,
    content: str,
    citations: Optional[List[Dict]] = None,
    metadata: Optional[Dict] = None,
) -> Dict[str, Any]:
    mid = str(uuid.uuid4())
    now = _now()
    with _get_conn() as conn:
        conn.execute(
            """INSERT INTO messages(id, session_id, role, content, citations, metadata, created_at)
               VALUES (?,?,?,?,?,?,?)""",
            (
                mid, session_id, role, content,
                json.dumps(citations or []),
                json.dumps(metadata or {}),
                now
            )
        )
        # bump session updated_at
        conn.execute(
            "UPDATE sessions SET updated_at=? WHERE id=?", (now, session_id)
        )
    return {
        "id": mid, "session_id": session_id, "role": role,
        "content": content, "citations": citations or [],
        "metadata": metadata or {}, "created_at": now
    }


def get_messages(session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM messages WHERE session_id=? ORDER BY created_at ASC LIMIT ?",
            (session_id, limit)
        ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d["citations"] = json.loads(d["citations"] or "[]")
        d["metadata"] = json.loads(d["metadata"] or "{}")
        result.append(d)
    return result


def clear_messages(session_id: str) -> int:
    with _get_conn() as conn:
        cur = conn.execute(
            "DELETE FROM messages WHERE session_id=?", (session_id,)
        )
    return cur.rowcount
