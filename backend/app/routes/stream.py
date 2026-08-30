"""
Streaming Chat Route — SSE (Server-Sent Events) streaming endpoint.

GET /api/stream?query=...&session_id=...&document_filter=...

Streams the LLM response token-by-token. Each SSE event has a JSON payload:
  {"type": "rewrite",   "rewritten_query": "..."}
  {"type": "retrieval", "docs_found": N}
  {"type": "token",     "text": "..."}           ← streamed LLM tokens
  {"type": "done",      "citations": [...], "latency_ms": N, ...}

Frontend: use EventSource or fetch with ReadableStream to consume.
"""
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from typing import Optional

from backend.app.services.rag_service import stream_rag_response
from backend.app.db import session_store

router = APIRouter()


@router.get("/stream")
async def stream_endpoint(
    query: str = Query(..., description="The safety/SOP query"),
    session_id: Optional[str] = Query(None, description="Active session ID for history"),
    document_filter: Optional[str] = Query(None, description="Restrict to a specific PDF filename"),
):
    if not query.strip():
        async def _error():
            import json
            yield f"data: {json.dumps({'type': 'error', 'message': 'Query cannot be empty.'})}\n\n"
        return StreamingResponse(_error(), media_type="text/event-stream")

    # Load history
    history = []
    if session_id and session_store.get_session(session_id):
        history = session_store.get_messages(session_id, limit=20)

    # Collect full response text for session persistence
    full_response = []

    async def _collect_and_stream():
        import json
        citations_out = []
        rewritten_out = query
        latency_out = 0

        async for chunk in stream_rag_response(query, history, document_filter):
            # chunk is already formatted as "data: {...}\n\n"
            yield chunk
            # Parse chunk to collect final state
            try:
                raw = chunk.removeprefix("data: ").strip()
                parsed = json.loads(raw)
                if parsed.get("type") == "token":
                    full_response.append(parsed.get("text", ""))
                elif parsed.get("type") == "done":
                    citations_out.extend(parsed.get("citations", []))
                    rewritten_out = parsed.get("rewritten_query", query)
                    latency_out = parsed.get("latency_ms", 0)
            except Exception:
                pass

        # Persist to session after stream completes
        if session_id and session_store.get_session(session_id):
            answer = "".join(full_response)
            session_store.add_message(session_id, "user", query)
            session_store.add_message(
                session_id, "assistant", answer,
                citations=citations_out,
                metadata={
                    "rewritten_query": rewritten_out,
                    "latency_ms": latency_out,
                    "mode": "streaming"
                }
            )

    return StreamingResponse(
        _collect_and_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # disable nginx buffering
        }
    )
