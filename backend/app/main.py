import os
import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import settings
from backend.app.middleware.auth import APIKeyMiddleware
from backend.app.db.session_store import init_db
from backend.app.services.document_manager import init_document_table, list_documents, register_document
from backend.app.services.ingest_service import ingest_pdf_manual
from backend.app.routes import (
    health_router,
    chat_router,
    stream_router,
    sessions_router,
    documents_router,
    telemetry_router,
)

# ── App init ───────────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Aegis AI — Sovereign On-Premise Agentic RAG Backend for MRPL Industrial Safety Manuals.\n\n"
        "Features:\n"
        "- Agentic RAG: query rewriting, multi-hop reasoning, self-critique\n"
        "- Hybrid Search: BM25 + ChromaDB dense vector with RRF fusion\n"
        "- Streaming SSE: real-time token-by-token LLM output\n"
        "- Session History: SQLite-backed conversation persistence\n"
        "- Document Manager: upload, list, delete, re-index PDFs\n"
        "- Telemetry: Ollama health, ChromaDB stats, system resources\n"
        "- Auth: optional API key guard\n"
        "- 100% Offline / Air-Gapped"
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Middleware ─────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "app://."],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(APIKeyMiddleware)

# ── Startup ────────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    """Initialize SQLite tables and auto-seed default MRPL SOP if empty."""
    init_db()
    init_document_table()

    # Ensure default SOP PDF exists on disk
    if not os.path.exists(settings.DEFAULT_SOP_PATH):
        try:
            from backend.app.create_sample_sop import generate_mrpl_safety_pdf
            print(f"[Aegis Startup] Pre-generating default SOP PDF: {settings.DEFAULT_SOP_PATH}")
            generate_mrpl_safety_pdf(settings.DEFAULT_SOP_PATH)
        except Exception as e:
            print(f"[Aegis Startup] Warning generating default SOP PDF: {e}")

    # Auto-seed default MRPL SOP if catalog is empty and file exists
    if settings.AUTO_SEED_DEFAULT_SOP and os.path.exists(settings.DEFAULT_SOP_PATH):
        try:
            existing = list_documents()
            if not existing:
                print(f"[Aegis Startup] Auto-indexing default SOP: {settings.DEFAULT_SOP_PATH}")
                result = ingest_pdf_manual(settings.DEFAULT_SOP_PATH)
                register_document(
                    doc_id=str(uuid.uuid4()),
                    filename=result["filename"],
                    filepath=result["filepath"],
                    total_pages=result["total_pages"],
                    total_chunks=result["total_chunks_indexed"],
                    file_size_kb=result["file_size_kb"],
                )
                print(f"[Aegis Startup] Predefined SOP indexed successfully ({result['total_chunks_indexed']} chunks).")
        except Exception as e:
            print(f"[Aegis Startup] Warning auto-seeding default SOP: {e}")


# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(health_router,    prefix="/api", tags=["Health"])
app.include_router(chat_router,      prefix="/api", tags=["Chat (RAG)"])
app.include_router(stream_router,    prefix="/api", tags=["Streaming (SSE)"])
app.include_router(sessions_router,  prefix="/api", tags=["Sessions"])
app.include_router(documents_router, prefix="/api", tags=["Documents"])
app.include_router(telemetry_router, prefix="/api", tags=["Telemetry"])


# ── Root ───────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "mode": "100% Offline / Air-Gapped",
        "docs": "/docs",
        "endpoints": {
            "health":    "GET  /api/health",
            "chat":      "POST /api/chat",
            "stream":    "GET  /api/stream?query=...",
            "sessions":  "CRUD /api/sessions",
            "documents": "CRUD /api/documents",
            "telemetry": "GET  /api/telemetry",
        }
    }
