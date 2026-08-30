"""
Telemetry Route — Live system health and performance metrics.

GET /api/telemetry

Returns:
  - Ollama connectivity + model info + available models list
  - ChromaDB collection stats (total chunks, collections)
  - Backend RAM / CPU usage (psutil if available, else N/A)
  - System uptime, Python version, session count
  - Agentic RAG config snapshot
"""
import sys
import time
from fastapi import APIRouter
import httpx

from backend.app.config import settings
from backend.app.db import session_store
from backend.app.services.document_manager import list_documents

router = APIRouter()

# Track server start time for uptime calculation
_SERVER_START = time.time()


@router.get("/telemetry")
async def get_telemetry():
    # ── Ollama status ──────────────────────────────────────────────────────────
    ollama_status = "disconnected"
    ollama_models = []
    ollama_latency_ms = None

    try:
        t0 = time.time()
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            ollama_latency_ms = int((time.time() - t0) * 1000)
            if resp.status_code == 200:
                ollama_status = "connected"
                data = resp.json()
                ollama_models = [
                    {
                        "name": m["name"],
                        "size_gb": round(m.get("size", 0) / 1e9, 2),
                        "modified": m.get("modified_at", ""),
                    }
                    for m in data.get("models", [])
                ]
    except Exception as e:
        ollama_status = f"error: {str(e)[:80]}"

    # ── ChromaDB stats ─────────────────────────────────────────────────────────
    chroma_chunks = -1
    chroma_collections = []
    try:
        from backend.app.services.ingest_service import get_vectorstore
        vs = get_vectorstore()
        chroma_chunks = vs._collection.count()
        chroma_collections = [vs._collection.name]
    except Exception:
        pass

    # ── System resources (optional psutil) ────────────────────────────────────
    ram_used_mb = None
    ram_total_mb = None
    cpu_percent = None
    try:
        import psutil
        proc = psutil.Process()
        ram_used_mb = round(proc.memory_info().rss / 1e6, 1)
        vm = psutil.virtual_memory()
        ram_total_mb = round(vm.total / 1e6, 1)
        cpu_percent = psutil.cpu_percent(interval=0.1)
    except ImportError:
        pass

    # ── Session stats ──────────────────────────────────────────────────────────
    sessions = session_store.list_sessions()
    documents = list_documents()

    uptime_s = int(time.time() - _SERVER_START)
    uptime_str = f"{uptime_s // 3600}h {(uptime_s % 3600) // 60}m {uptime_s % 60}s"

    return {
        "system": {
            "project": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "python_version": sys.version.split()[0],
            "uptime": uptime_str,
            "mode": "100% Offline / Air-Gapped",
        },
        "ollama": {
            "status": ollama_status,
            "base_url": settings.OLLAMA_BASE_URL,
            "active_llm": settings.LLM_MODEL,
            "active_embedding": settings.EMBEDDING_MODEL,
            "latency_ms": ollama_latency_ms,
            "available_models": ollama_models,
        },
        "vectorstore": {
            "type": "ChromaDB",
            "total_chunks": chroma_chunks,
            "collections": chroma_collections,
            "vector_db_dir": settings.VECTOR_DB_DIR,
        },
        "rag_config": {
            "retrieval_k": settings.RETRIEVAL_K,
            "bm25_weight": settings.BM25_WEIGHT,
            "max_hops": settings.MAX_HOPS,
            "rewrite_query": settings.REWRITE_QUERY,
            "self_critique": settings.SELF_CRITIQUE,
        },
        "data": {
            "total_sessions": len(sessions),
            "total_documents": len(documents),
            "documents": documents,
        },
        "resources": {
            "ram_used_mb": ram_used_mb,
            "ram_total_mb": ram_total_mb,
            "cpu_percent": cpu_percent,
        },
        "auth": {
            "api_key_enabled": bool(settings.API_KEY),
        }
    }
