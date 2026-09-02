import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App Details
    APP_NAME: str = "PRAHARI AI - Industrial Safety Copilot"
    VERSION: str = "2.7.4"

    # Ollama Local LLM & Embeddings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "llama3.2"
    EMBEDDING_MODEL: str = "nomic-embed-text"

    # Agentic RAG settings
    RETRIEVAL_K: int = 6           # top-k chunks from hybrid retrieval
    BM25_WEIGHT: float = 0.4       # weight for BM25 score in hybrid fusion (0 = pure vector, 1 = pure BM25)
    MAX_HOPS: int = 2              # max reasoning hops in multi-hop RAG
    REWRITE_QUERY: bool = True     # enable automatic query rewriting
    SELF_CRITIQUE: bool = True     # enable self-critique / answer validation pass
    AUTO_SEED_DEFAULT_SOP: bool = True # automatically index default MRPL SOP on startup if empty

    # Auth
    API_KEY: Optional[str] = None  # if set, all /api/* routes require X-API-Key header

    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    UPLOAD_DIR: str = os.path.join(DATA_DIR, "uploads")
    VECTOR_DB_DIR: str = os.path.join(DATA_DIR, "vectorstore")
    SESSION_DB_PATH: str = os.path.join(DATA_DIR, "sessions.db")
    DEFAULT_SOP_PATH: str = os.path.join(BASE_DIR, "MRPL_Refinery_Safety_SOP_2026.pdf")

    class Config:
        env_file = ".env"


settings = Settings()

# Ensure directories exist at import time
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.VECTOR_DB_DIR, exist_ok=True)
