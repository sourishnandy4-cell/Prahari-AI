"""
Session Management Routes.

POST   /api/sessions              — create new session
GET    /api/sessions              — list all sessions
GET    /api/sessions/{id}         — get session metadata
PATCH  /api/sessions/{id}         — rename session
DELETE /api/sessions/{id}         — delete session + all messages
GET    /api/sessions/{id}/messages — get all messages in session
DELETE /api/sessions/{id}/messages — clear all messages in session
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.app.db import session_store

router = APIRouter()


class CreateSessionRequest(BaseModel):
    title: Optional[str] = "New Session"


class RenameSessionRequest(BaseModel):
    title: str


# ── Session CRUD ───────────────────────────────────────────────────────────────

@router.post("/sessions", status_code=201)
async def create_session(body: CreateSessionRequest):
    return session_store.create_session(body.title)


@router.get("/sessions")
async def list_sessions():
    return {"sessions": session_store.list_sessions()}


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    sess = session_store.get_session(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    return sess


@router.patch("/sessions/{session_id}")
async def rename_session(session_id: str, body: RenameSessionRequest):
    ok = session_store.rename_session(session_id, body.title)
    if not ok:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"success": True, "session_id": session_id, "title": body.title}


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    ok = session_store.delete_session(session_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"success": True, "deleted_session_id": session_id}


# ── Messages ───────────────────────────────────────────────────────────────────

@router.get("/sessions/{session_id}/messages")
async def get_messages(session_id: str, limit: int = 50):
    sess = session_store.get_session(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    messages = session_store.get_messages(session_id, limit=limit)
    return {"session_id": session_id, "messages": messages, "count": len(messages)}


@router.delete("/sessions/{session_id}/messages")
async def clear_messages(session_id: str):
    sess = session_store.get_session(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    deleted = session_store.clear_messages(session_id)
    return {"success": True, "session_id": session_id, "messages_deleted": deleted}
