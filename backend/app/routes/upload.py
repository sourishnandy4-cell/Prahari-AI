from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from langchain_core.documents import Document
from backend.app.config import settings
from backend.app.services.ingest_service import ingest_pdf_manual, get_vectorstore
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Ingest PDF into ChromaDB
        if ext == ".pdf":
            result = ingest_pdf_manual(file_path)
            return result
            
        # Ingest Text/Markdown/CSV into ChromaDB
        elif ext in [".txt", ".md", ".csv", ".json"]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                raw_text = f.read()
            
            splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
            text_chunks = splitter.split_text(raw_text)
            
            docs = []
            for i, chunk in enumerate(text_chunks):
                docs.append(Document(
                    page_content=chunk,
                    metadata={
                        "chunk_id": str(uuid.uuid4()),
                        "source": os.path.abspath(file_path),
                        "filepath": os.path.abspath(file_path),
                        "filename": filename,
                        "page": i + 1,
                    }
                ))
            
            vectorstore = get_vectorstore()
            if docs:
                vectorstore.add_documents(docs)
                
            return {
                "status": "success",
                "filename": filename,
                "filepath": os.path.abspath(file_path),
                "total_pages": 1,
                "total_chunks_indexed": len(docs),
                "file_size_kb": round(os.path.getsize(file_path) / 1024, 2),
                "type": "document"
            }
            
        # Handle Images (Diagrams, Blueprints, Photos)
        elif ext in [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".svg"]:
            return {
                "status": "success",
                "filename": filename,
                "filepath": os.path.abspath(file_path),
                "file_size_kb": round(os.path.getsize(file_path) / 1024, 2),
                "type": "image",
                "message": "Image attached and ready for safety vision analysis."
            }
        else:
            return {
                "status": "success",
                "filename": filename,
                "filepath": os.path.abspath(file_path),
                "file_size_kb": round(os.path.getsize(file_path) / 1024, 2),
                "type": "file"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process uploaded file: {str(e)}")

