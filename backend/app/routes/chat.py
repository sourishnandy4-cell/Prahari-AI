"""
Chat Route — Standard (non-streaming) RAG endpoint.

POST /api/chat
Body: { "query": "...", "session_id": "...", "document_filter": "..." }

Supports optional session persistence — if session_id is provided, the conversation
is automatically stored in SQLite and history is injected into the RAG prompt.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import asyncio

from backend.app.services.rag_service import query_rag_engine
from backend.app.db import session_store

router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None     # if provided, history is loaded and message is saved
    document_filter: Optional[str] = None  # restrict RAG to a specific filename


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Load conversation history for context injection
    history = []
    session_id = request.session_id
    if session_id:
        if not session_store.get_session(session_id):
            raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")
        history = session_store.get_messages(session_id, limit=20)

    try:
        result = await asyncio.to_thread(
            query_rag_engine,
            request.query,
            history,
            request.document_filter,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG execution failed: {str(e)}")

    # Persist messages if session is active
    if session_id:
        session_store.add_message(session_id, "user", request.query)
        session_store.add_message(
            session_id, "assistant", result["answer"],
            citations=result.get("citations"),
            metadata={
                "model": result.get("model"),
                "mode": result.get("mode"),
                "hops": result.get("hops"),
                "latency_ms": result.get("latency_ms"),
            }
        )

    return result
