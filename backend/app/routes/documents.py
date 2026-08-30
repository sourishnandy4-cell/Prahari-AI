"""
Document Management Routes.

POST   /api/upload                        — upload & ingest a PDF (existing, now enhanced)
GET    /api/documents                     — list all indexed documents with metadata
GET    /api/documents/stats               — ChromaDB collection stats + per-doc chunk counts
DELETE /api/documents/{doc_id}            — delete document from disk + ChromaDB
POST   /api/documents/{doc_id}/reindex    — re-run full ingestion pipeline for a document
"""
import os
import uuid
import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.app.config import settings
from backend.app.services.ingest_service import ingest_pdf_manual
from backend.app.services.document_manager import (
    register_document,
    list_documents,
    delete_document,
    reindex_document,
    get_collection_stats,
    get_document_by_id,
    init_document_table,
)

router = APIRouter()


@router.post("/upload", status_code=201)
async def upload_document(file: UploadFile = File(...)):
    """Upload a manual/document/attachment, ingest into ChromaDB if text/PDF, and register in document tracking DB."""
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    allowed_docs = [".pdf", ".txt", ".md", ".csv", ".json", ".doc", ".docx"]
    allowed_images = [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".svg"]

    if ext not in allowed_docs and ext not in allowed_images:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: '{ext}'. Supported formats: PDF, TXT, MD, CSV, JSON, and Images."
        )

    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    try:
        # Save to disk (non-blocking read then write)
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        file_size_kb = round(os.path.getsize(file_path) / 1024, 2)

        # Ingest PDF
        if ext == ".pdf":
            result = await asyncio.to_thread(ingest_pdf_manual, file_path)
            doc_id = str(uuid.uuid4())
            doc = register_document(
                doc_id=doc_id,
                filename=result["filename"],
                filepath=result["filepath"],
                total_pages=result["total_pages"],
                total_chunks=result["total_chunks_indexed"],
                file_size_kb=result["file_size_kb"],
            )
            return {**result, "doc_id": doc.get("id", doc_id), "type": "pdf"}

        # Ingest Text/Markdown/CSV/JSON
        elif ext in [".txt", ".md", ".csv", ".json"]:
            def _ingest_text_file(path: str, fname: str):
                from langchain_core.documents import Document
                from langchain_text_splitters import RecursiveCharacterTextSplitter
                from backend.app.services.ingest_service import get_vectorstore

                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    raw_text = f.read()

                splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
                text_chunks = splitter.split_text(raw_text)

                docs = []
                for i, chunk in enumerate(text_chunks):
                    docs.append(Document(
                        page_content=chunk,
                        metadata={
                            "chunk_id": str(uuid.uuid4()),
                            "source": os.path.abspath(path),
                            "filepath": os.path.abspath(path),
                            "filename": fname,
                            "page": i + 1,
                        }
                    ))

                vs = get_vectorstore()
                if docs:
                    vs.add_documents(docs)

                return {
                    "status": "success",
                    "filename": fname,
                    "filepath": os.path.abspath(path),
                    "total_pages": max(1, len(docs) // 3),
                    "total_chunks_indexed": len(docs),
                    "file_size_kb": round(os.path.getsize(path) / 1024, 2),
                    "type": "document"
                }

            result = await asyncio.to_thread(_ingest_text_file, file_path, filename)
            doc_id = str(uuid.uuid4())
            doc = register_document(
                doc_id=doc_id,
                filename=result["filename"],
                filepath=result["filepath"],
                total_pages=result["total_pages"],
                total_chunks=result["total_chunks_indexed"],
                file_size_kb=result["file_size_kb"],
            )
            return {**result, "doc_id": doc.get("id", doc_id)}

        # Image Attachments
        elif ext in allowed_images:
            return {
                "status": "success",
                "filename": filename,
                "filepath": os.path.abspath(file_path),
                "file_size_kb": file_size_kb,
                "type": "image",
                "message": "Image attached and ready for safety vision analysis."
            }

        else:
            return {
                "status": "success",
                "filename": filename,
                "filepath": os.path.abspath(file_path),
                "file_size_kb": file_size_kb,
                "type": "file"
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process uploaded file: {str(e)}")


@router.get("/documents")
async def list_all_documents():
    """Return all indexed documents with ingestion metadata."""
    return {"documents": list_documents()}


@router.get("/documents/stats")
async def collection_stats():
    """Return ChromaDB collection stats, total chunks, and per-document breakdown."""
    return get_collection_stats()


@router.delete("/documents/{doc_id}")
async def delete_doc(doc_id: str):
    """Remove document from disk, ChromaDB, and tracking DB."""
    doc = get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    result = await asyncio.to_thread(delete_document, doc_id)
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Deletion failed"))
    return result


@router.post("/documents/{doc_id}/reindex")
async def reindex_doc(doc_id: str):
    """Re-run ingestion pipeline for an already-uploaded document."""
    doc = get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    result = await asyncio.to_thread(reindex_document, doc_id)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message", "Re-indexing failed"))
    return result
