import os
import uuid
from contextlib import asynccontextmanager
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
    bis_router,
)


# ── Lifespan (replaces deprecated @app.on_event) ───────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize SQLite tables and auto-seed default MRPL SOP & BIS Standards if empty."""
    init_db()
    init_document_table()

    # 1. Ensure default SOP PDF exists on disk
    if not os.path.exists(settings.DEFAULT_SOP_PATH):
        try:
            from backend.app.create_sample_sop import generate_mrpl_safety_pdf
            print(f"[Startup] Pre-generating default MRPL SOP PDF: {settings.DEFAULT_SOP_PATH}")
            generate_mrpl_safety_pdf(settings.DEFAULT_SOP_PATH)
        except Exception as e:
            print(f"[Startup] Warning generating default SOP PDF: {e}")

    # 2. Ensure BIS Standards Compendium PDF exists on disk
    if not os.path.exists(settings.DEFAULT_BIS_PATH):
        try:
            from backend.app.create_sample_bis_compendium import generate_bis_compendium_pdf
            print(f"[Startup] Pre-generating BIS Standards Compendium PDF: {settings.DEFAULT_BIS_PATH}")
            generate_bis_compendium_pdf(settings.DEFAULT_BIS_PATH)
        except Exception as e:
            print(f"[Startup] Warning generating BIS Compendium PDF: {e}")

    # Auto-seed documents into catalog & vectorstore
    try:
        existing = list_documents()
        existing_filenames = [d["filename"] for d in existing]

        # Auto-seed default MRPL SOP
        if settings.AUTO_SEED_DEFAULT_SOP and os.path.exists(settings.DEFAULT_SOP_PATH):
            sop_name = os.path.basename(settings.DEFAULT_SOP_PATH)
            if sop_name not in existing_filenames:
                print(f"[Startup] Auto-indexing default MRPL SOP: {settings.DEFAULT_SOP_PATH}")
                result = ingest_pdf_manual(settings.DEFAULT_SOP_PATH)
                register_document(
                    doc_id=str(uuid.uuid4()),
                    filename=result["filename"],
                    filepath=result["filepath"],
                    total_pages=result["total_pages"],
                    total_chunks=result["total_chunks_indexed"],
                    file_size_kb=result["file_size_kb"],
                )
                print(f"[Startup] Predefined SOP indexed ({result['total_chunks_indexed']} chunks).")

        # Auto-seed BIS Standards Compendium
        if settings.AUTO_SEED_BIS_STANDARDS and os.path.exists(settings.DEFAULT_BIS_PATH):
            bis_name = os.path.basename(settings.DEFAULT_BIS_PATH)
            if bis_name not in existing_filenames:
                print(f"[Startup] Auto-indexing BIS Standards Compendium: {settings.DEFAULT_BIS_PATH}")
                bis_result = ingest_pdf_manual(settings.DEFAULT_BIS_PATH)
                register_document(
                    doc_id=str(uuid.uuid4()),
                    filename=bis_result["filename"],
                    filepath=bis_result["filepath"],
                    total_pages=bis_result["total_pages"],
                    total_chunks=bis_result["total_chunks_indexed"],
                    file_size_kb=bis_result["file_size_kb"],
                )
                print(f"[Startup] BIS Standards Compendium indexed ({bis_result['total_chunks_indexed']} chunks).")
    except Exception as e:
        print(f"[Startup] Warning auto-seeding documents: {e}")

    yield  # App runs here
    # (Shutdown logic can go here if needed)


# ── App init ───────────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
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
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "app://.",
        # Allow LAN IP connections for Android APK (all 192.168.x.x / 10.x.x.x)
        "*",
    ],
    allow_credentials=False,   # must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(APIKeyMiddleware)


app.include_router(health_router,    prefix="/api", tags=["Health"])
app.include_router(chat_router,      prefix="/api", tags=["Chat (RAG)"])
app.include_router(stream_router,    prefix="/api", tags=["Streaming (SSE)"])
app.include_router(sessions_router,  prefix="/api", tags=["Sessions"])
app.include_router(documents_router, prefix="/api", tags=["Documents"])
app.include_router(telemetry_router, prefix="/api", tags=["Telemetry"])
app.include_router(bis_router,       prefix="/api", tags=["BIS Standards"])


# ── Root ───────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    return {
        "system": settings.PROJECT_NAME,
        "sih_problem": "26107 - AI Virtual Assistant for Indian Standards & BIS Schemes",
        "version": settings.VERSION,
        "status": "online",
        "mode": "Dual Engine (Local Ollama + Sovereign Offline Intelligence)",
        "docs": "/docs",
        "endpoints": {
            "health":     "GET  /api/health",
            "ping":       "GET  /api/ping",
            "chat":       "POST /api/chat",
            "stream":     "GET  /api/stream?query=...",
            "sessions":   "CRUD /api/sessions",
            "documents":  "CRUD /api/documents",
            "telemetry":  "GET  /api/telemetry",
            "bis_standards": "GET /api/bis/standards",
            "bis_categories": "GET /api/bis/categories",
            "bis_compare": "POST /api/bis/compare",
            "bis_huid": "POST /api/bis/verify-huid",
            "bis_cml": "POST /api/bis/verify-cml",
            "bis_steps": "GET /api/bis/certification-steps",
            "bis_helpline": "GET /api/bis/helpline",
        }
    }


# ── Ping (lightweight health for mobile / Electron) ─────────────────────────────
@app.get("/api/ping", tags=["Health"])
async def ping():
    """Ultra-lightweight ping for Capacitor APK and Electron health polling."""
    return {"status": "ok", "version": settings.VERSION}


# ── Standalone Entrypoint for PyInstaller / Aegis Backend Executable ───────────
if __name__ == "__main__":
    import sys
    import uvicorn

    host = "127.0.0.1"
    port = 8000

    for i, arg in enumerate(sys.argv):
        if arg == "--host" and i + 1 < len(sys.argv):
            host = sys.argv[i + 1]
        elif arg == "--port" and i + 1 < len(sys.argv):
            try:
                port = int(sys.argv[i + 1])
            except ValueError:
                pass

    print(f"[PRAHARI Backend] Starting server on {host}:{port} (100% Offline / Air-Gapped)...")
    uvicorn.run(app, host=host, port=port, log_level="info")

