"""
Deprecated Route: /api/upload
Superseded by backend/app/routes/documents.py
This module is maintained for backward compatibility.
"""
from fastapi import APIRouter, UploadFile, File
from backend.app.routes.documents import upload_document as doc_upload_handler

router = APIRouter()


@router.post("/upload", status_code=201, deprecated=True)
async def upload_document(file: UploadFile = File(...)):
    """Deprecated endpoint — delegates directly to documents.upload_document."""
    return await doc_upload_handler(file=file)
