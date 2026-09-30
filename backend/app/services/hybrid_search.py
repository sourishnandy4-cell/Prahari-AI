import os
import time
from typing import List, Dict, Any, Optional
from rank_bm25 import BM25Okapi
from langchain_core.documents import Document
from backend.app.config import settings
from backend.app.services.ingest_service import get_vectorstore


# ── In-Memory BM25 Index Cache ────────────────────────────────────────────────
_bm25_cache = {
    "corpus_docs": [],
    "bm25_instance": None,
    "last_count": -1,
    "last_updated": 0.0,
}


def invalidate_bm25_cache() -> None:
    """Invalidates the in-memory BM25 index cache when documents are modified."""
    global _bm25_cache
    _bm25_cache = {
        "corpus_docs": [],
        "bm25_instance": None,
        "last_count": -1,
        "last_updated": 0.0,
    }


def _rrf_score(rank: int, k: int = 60) -> float:
    """Reciprocal Rank Fusion score: 1 / (k + rank)."""
    return 1.0 / (k + rank + 1)


def hybrid_retrieve(
    query: str,
    k: int = None,
    bm25_weight: float = None,
    document_filter: Optional[str] = None
) -> List[Document]:
    """
    Hybrid Search: Dense Vector Retrieval (ChromaDB) + Global Sparse Lexical Search (BM25)
    fused using Reciprocal Rank Fusion (RRF).

    Caches the BM25 index in memory to avoid full-corpus re-tokenization on every retrieval.
    """
    global _bm25_cache
    if k is None:
        k = settings.RETRIEVAL_K
    if bm25_weight is None:
        bm25_weight = settings.BM25_WEIGHT

    vectorstore = get_vectorstore()
    fetch_k = max(k * 4, 16)

    # ── 1. Fetch & Cache Corpus Chunks for BM25 ─────────────────────────────────
    current_count = -1
    try:
        current_count = vectorstore._collection.count()
    except Exception:
        pass

    cache_valid = (
        _bm25_cache["bm25_instance"] is not None
        and _bm25_cache["last_count"] == current_count
        and current_count > 0
    )

    if cache_valid:
        all_corpus_docs = _bm25_cache["corpus_docs"]
        bm25 = _bm25_cache["bm25_instance"]
    else:
        all_corpus_docs = []
        try:
            raw_collection = vectorstore._collection.get()
            if raw_collection and raw_collection.get("documents"):
                for idx, doc_text in enumerate(raw_collection["documents"]):
                    meta = raw_collection["metadatas"][idx] if raw_collection.get("metadatas") else {}
                    all_corpus_docs.append(Document(page_content=doc_text, metadata=meta))
        except Exception:
            pass

        if all_corpus_docs:
            corpus = [doc.page_content for doc in all_corpus_docs]
            tokenized = [text.lower().split() for text in corpus]
            bm25 = BM25Okapi(tokenized)
            _bm25_cache["corpus_docs"] = all_corpus_docs
            _bm25_cache["bm25_instance"] = bm25
            _bm25_cache["last_count"] = current_count
            _bm25_cache["last_updated"] = time.time()
        else:
            bm25 = None

    # If no documents in database, return empty
    if not all_corpus_docs:
        return []

    # ── 2. Dense Vector Search ──────────────────────────────────────────────────
    dense_docs: List[Document] = []
    try:
        if document_filter:
            where_filter = {
                "$or": [
                    {"filename": {"$eq": document_filter}},
                    {"filepath": {"$eq": document_filter}},
                    {"source": {"$eq": document_filter}}
                ]
            }
            try:
                dense_docs = vectorstore.similarity_search(query, k=fetch_k, filter=where_filter)
            except Exception:
                try:
                    dense_docs = vectorstore.similarity_search(query, k=fetch_k, filter={"filename": document_filter})
                except Exception:
                    dense_docs = vectorstore.similarity_search(query, k=fetch_k)
        else:
            dense_docs = vectorstore.similarity_search(query, k=fetch_k)
    except Exception:
        dense_docs = []

    # If dense search returned empty, use the first N docs as fallback dense
    if not dense_docs:
        dense_docs = all_corpus_docs[:fetch_k]

    # Filter dense docs in memory if filter was specified
    if document_filter:
        df_lower = document_filter.lower()
        dense_docs = [
            d for d in dense_docs
            if df_lower in d.metadata.get("filename", "").lower()
            or df_lower in d.metadata.get("filepath", "").lower()
            or df_lower in d.metadata.get("source", "").lower()
        ]

    # ── 3. Global Sparse Lexical Search (BM25) Across ALL Documents ─────────────
    bm25_ranked: List[Document] = []
    query_tokens = [w for w in query.lower().replace("?", "").replace(",", "").replace(".", "").split() if len(w) > 1]
    if not query_tokens:
        query_tokens = query.lower().split()

    if bm25 and query_tokens:
        bm25_scores = bm25.get_scores(query_tokens)

        # Sort all corpus documents by BM25 score
        bm25_indexed = sorted(
            enumerate(all_corpus_docs),
            key=lambda x: bm25_scores[x[0]],
            reverse=True
        )
        if document_filter:
            df_lower = document_filter.lower()
            filtered = []
            for idx, _ in bm25_indexed:
                d = all_corpus_docs[idx]
                if (df_lower in d.metadata.get("filename", "").lower()
                    or df_lower in d.metadata.get("filepath", "").lower()
                    or df_lower in d.metadata.get("source", "").lower()):
                    filtered.append(d)
                if len(filtered) >= fetch_k:
                    break
            bm25_ranked = filtered
        else:
            bm25_ranked = [all_corpus_docs[idx] for idx, _ in bm25_indexed[:fetch_k]]
    else:
        bm25_ranked = all_corpus_docs[:fetch_k]

    # ── 4. Reciprocal Rank Fusion (RRF) ─────────────────────────────────────────
    doc_rrf: Dict[str, float] = {}
    doc_obj: Dict[str, Document] = {}

    for rank, doc in enumerate(dense_docs):
        key = f"{doc.metadata.get('filename','')}:{doc.metadata.get('page','')}:{doc.page_content[:80]}"
        doc_rrf.setdefault(key, 0.0)
        doc_rrf[key] += (1.0 - bm25_weight) * _rrf_score(rank)
        doc_obj[key] = doc

    for rank, doc in enumerate(bm25_ranked):
        key = f"{doc.metadata.get('filename','')}:{doc.metadata.get('page','')}:{doc.page_content[:80]}"
        doc_rrf.setdefault(key, 0.0)
        doc_rrf[key] += bm25_weight * _rrf_score(rank)
        doc_obj[key] = doc

    # Sort by combined fused score
    sorted_keys = sorted(doc_rrf, key=lambda x: doc_rrf[x], reverse=True)
    results = [doc_obj[key] for key in sorted_keys[:k]]

    return results if results else all_corpus_docs[:k]
