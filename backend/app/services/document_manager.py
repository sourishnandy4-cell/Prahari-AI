"""
Document Manager — tracks uploaded PDFs and their ChromaDB collection state.

Provides:
  - list_documents()     : all PDFs + ingestion metadata
  - delete_document()    : remove PDF file + purge its chunks from ChromaDB
  - reindex_document()   : re-run full ingest pipeline for an already-uploaded file
  - get_collection_stats(): chunk counts, embedding model info

All metadata is stored in a lightweight SQLite table (reuses the same DB as sessions).
"""
import os
import json
import sqlite3
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


def init_document_table() -> None:
    """Create document tracking table. Called once at app startup."""
    with _get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS documents (
                id            TEXT PRIMARY KEY,
                filename      TEXT NOT NULL UNIQUE,
                filepath      TEXT NOT NULL,
                total_pages   INTEGER DEFAULT 0,
                total_chunks  INTEGER DEFAULT 0,
                file_size_kb  REAL DEFAULT 0,
                ingested_at   TEXT NOT NULL,
                reindexed_at  TEXT
            );
        """)


# ── Document CRUD ──────────────────────────────────────────────────────────────

def register_document(
    doc_id: str,
    filename: str,
    filepath: str,
    total_pages: int,
    total_chunks: int,
    file_size_kb: float,
) -> Dict[str, Any]:
    now = _now()
    with _get_conn() as conn:
        conn.execute(
            """INSERT INTO documents(id, filename, filepath, total_pages, total_chunks, file_size_kb, ingested_at)
               VALUES (?,?,?,?,?,?,?)
               ON CONFLICT(filename) DO UPDATE SET
                 total_pages=excluded.total_pages,
                 total_chunks=excluded.total_chunks,
                 file_size_kb=excluded.file_size_kb,
                 reindexed_at=excluded.ingested_at""",
            (doc_id, filename, filepath, total_pages, total_chunks, file_size_kb, now)
        )
    return get_document_by_filename(filename)


def list_documents() -> List[Dict[str, Any]]:
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM documents ORDER BY ingested_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def get_document_by_filename(filename: str) -> Optional[Dict[str, Any]]:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM documents WHERE filename=?", (filename,)
        ).fetchone()
    return dict(row) if row else None


def get_document_by_id(doc_id: str) -> Optional[Dict[str, Any]]:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM documents WHERE id=?", (doc_id,)
        ).fetchone()
    return dict(row) if row else None


def delete_document(doc_id: str) -> Dict[str, Any]:
    """
    Remove document from:
      1. The documents tracking table
      2. The physical file on disk
      3. ChromaDB — purge all chunks whose metadata source matches the filename
    """
    doc = get_document_by_id(doc_id)
    if not doc:
        return {"success": False, "error": "Document not found"}

    filename = doc["filename"]
    filepath = doc["filepath"]
    errors = []

    # 1. Remove from ChromaDB
    try:
        from backend.app.services.ingest_service import get_vectorstore
        vs = get_vectorstore()
        collection = vs._collection  # access underlying chromadb Collection
        # Query by metadata source filter
        results = collection.get(where={"source": filepath})
        if results and results.get("ids"):
            collection.delete(ids=results["ids"])
    except Exception as e:
        errors.append(f"ChromaDB purge warning: {e}")

    # 2. Remove physical file
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        errors.append(f"File removal warning: {e}")

    # 3. Remove from DB
    with _get_conn() as conn:
        conn.execute("DELETE FROM documents WHERE id=?", (doc_id,))

    return {
        "success": True,
        "deleted_filename": filename,
        "warnings": errors
    }


def reindex_document(doc_id: str) -> Dict[str, Any]:
    """Re-run the ingestion pipeline for an already-uploaded file."""
    doc = get_document_by_id(doc_id)
    if not doc:
        return {"status": "error", "message": "Document not found"}

    filepath = doc["filepath"]
    if not os.path.exists(filepath):
        return {"status": "error", "message": f"File not found on disk: {filepath}"}

    # First purge existing chunks for this file
    try:
        from backend.app.services.ingest_service import get_vectorstore
        vs = get_vectorstore()
        collection = vs._collection
        results = collection.get(where={"source": filepath})
        if results and results.get("ids"):
            collection.delete(ids=results["ids"])
    except Exception:
        pass  # best effort

    # Re-ingest
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        from backend.app.services.ingest_service import ingest_pdf_manual
        result = ingest_pdf_manual(filepath)
    elif ext in [".txt", ".md", ".csv", ".json"]:
        import uuid
        from langchain_core.documents import Document
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from backend.app.services.ingest_service import get_vectorstore

        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()

        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        text_chunks = splitter.split_text(raw_text)

        docs = []
        for i, chunk in enumerate(text_chunks):
            docs.append(Document(
                page_content=chunk,
                metadata={
                    "chunk_id": str(uuid.uuid4()),
                    "source": os.path.abspath(filepath),
                    "filepath": os.path.abspath(filepath),
                    "filename": doc["filename"],
                    "page": i + 1,
                }
            ))

        vs = get_vectorstore()
        if docs:
            vs.add_documents(docs)

        result = {
            "status": "success",
            "filename": doc["filename"],
            "filepath": os.path.abspath(filepath),
            "total_pages": max(1, len(docs) // 3),
            "total_chunks_indexed": len(docs),
            "file_size_kb": round(os.path.getsize(filepath) / 1024, 2),
        }
    else:
        result = {
            "status": "success",
            "filename": doc["filename"],
            "filepath": os.path.abspath(filepath),
            "total_pages": 1,
            "total_chunks_indexed": 0,
            "file_size_kb": round(os.path.getsize(filepath) / 1024, 2),
        }

    # Update DB
    now = _now()
    with _get_conn() as conn:
        conn.execute(
            "UPDATE documents SET total_pages=?, total_chunks=?, reindexed_at=? WHERE id=?",
            (result.get("total_pages", 0), result.get("total_chunks_indexed", 0), now, doc_id)
        )

    return {**result, "reindexed_at": now}


def get_collection_stats() -> Dict[str, Any]:
    """Return total chunks in ChromaDB and per-document breakdown."""
    try:
        from backend.app.services.ingest_service import get_vectorstore
        vs = get_vectorstore()
        collection = vs._collection
        total = collection.count()
    except Exception as e:
        total = -1

    docs = list_documents()
    return {
        "total_chunks_in_vectorstore": total,
        "total_documents": len(docs),
        "embedding_model": settings.EMBEDDING_MODEL,
        "vector_db_dir": settings.VECTOR_DB_DIR,
        "documents": docs,
    }
