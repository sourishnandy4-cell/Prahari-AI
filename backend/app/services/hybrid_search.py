import os
from typing import List, Dict, Any, Optional
from rank_bm25 import BM25Okapi
from langchain_core.documents import Document
from backend.app.config import settings
from backend.app.services.ingest_service import get_vectorstore


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

    Searches the entire document corpus using BM25 and combines with Dense semantic vectors.
    """
    if k is None:
        k = settings.RETRIEVAL_K
    if bm25_weight is None:
        bm25_weight = settings.BM25_WEIGHT

    vectorstore = get_vectorstore()
    fetch_k = max(k * 4, 16)

    # ── 1. Fetch All Available Chunks from ChromaDB Collection for Global BM25 ──
    all_corpus_docs: List[Document] = []
    try:
        raw_collection = vectorstore._collection.get()
        if raw_collection and raw_collection.get("documents"):
            for idx, doc_text in enumerate(raw_collection["documents"]):
                meta = raw_collection["metadatas"][idx] if raw_collection.get("metadatas") else {}
                doc = Document(page_content=doc_text, metadata=meta)
                # Apply document_filter if present
                if document_filter:
                    df_lower = document_filter.lower()
                    fn = meta.get("filename", "").lower()
                    fp = meta.get("filepath", "").lower()
                    src = meta.get("source", "").lower()
                    if df_lower not in fn and df_lower not in fp and df_lower not in src:
                        continue
                all_corpus_docs.append(doc)
    except Exception:
        pass

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

    if all_corpus_docs and query_tokens:
        corpus = [doc.page_content for doc in all_corpus_docs]
        tokenized = [text.lower().split() for text in corpus]
        bm25 = BM25Okapi(tokenized)
        bm25_scores = bm25.get_scores(query_tokens)

        # Sort all corpus documents by BM25 score
        bm25_indexed = sorted(
            enumerate(all_corpus_docs),
            key=lambda x: bm25_scores[x[0]],
            reverse=True
        )
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
