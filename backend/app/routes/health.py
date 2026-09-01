from fastapi import APIRouter
import httpx
from backend.app.config import settings

router = APIRouter()


@router.get("/health")
async def check_health():
    """Quick liveness check — use /api/telemetry for full system metrics."""
    ollama_status = "disconnected"
    try:
        async with httpx.AsyncClient(timeout=0.6) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if resp.status_code == 200:
                ollama_status = "connected"
    except Exception:
        ollama_status = "unreachable"

    return {
        "status": "ok",
        "version": settings.VERSION,
        "ollama_engine": settings.OLLAMA_BASE_URL,
        "ollama_status": ollama_status,
        "active_llm": settings.LLM_MODEL,
        "active_embeddings": settings.EMBEDDING_MODEL,
        "mode": "Air-Gapped",
    }
