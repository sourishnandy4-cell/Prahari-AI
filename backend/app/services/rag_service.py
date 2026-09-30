import os
import re
import time
import asyncio
from typing import List, Dict, Any, Optional, AsyncGenerator
import httpx
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

from backend.app.config import settings
from backend.app.services.hybrid_search import hybrid_retrieve
from backend.app.services.offline_intelligence import offline_intelligence
from backend.app.services.online_ai_service import (
    is_internet_connected,
    search_live_web,
    call_gemini_cloud_llm,
    synthesize_online_response,
)


# ── Prompts ────────────────────────────────────────────────────────────────────

ANSWER_PROMPT = """You are PRAHARI AI, the authoritative Virtual Assistant for Indian Standards (IS codes), Bureau of Indian Standards (BIS) Schemes (SIH Topic 26107), and Industrial Engineering & Operational Safety.

Guidelines:
1. When answering questions regarding Indian Standards (IS codes), BIS certification schemes (Scheme-I, CRS Scheme-II, FMCS), ISI mark verification, Gold/Silver hallmarking (6-digit HUID), consumer complaints, or quality control orders (QCO):
   - ALWAYS name the exact Standard Number (e.g. IS 10500:2012, IS 14543:2004, IS 1293:2019, IS 1786:2008, IS 1417:2016) and the specific Clause it came from.
   - For industry Q&A ('Which IS standard applies to my product?' or 'What testing is needed?'), state the exact standard, QCO compliance status, and mandatory routine/type tests.
   - For consumer Q&A, explain ISI mark checks (7-digit CML number), Gold Hallmark verification (3 marks: BIS logo, Fineness, 6-digit HUID), and complaint process via the BIS Care App and National Consumer Helpline (1800-11-1255 / 1915).
   - If the user asks in Hindi, answer in clear, polite Hindi with accurate technical terminology.
   - "I don't know" handling: If the answer is not in the documents or repository, explicitly state so and point to the BIS Toll-Free Helpline (1800-11-1255) and official portal (www.bis.gov.in) instead of guessing.
2. When the query relates to MRPL refinery safety, emergency shutdowns, H2S limits, PSV testing, or hazardous zone permits, strictly ground your response in the provided MRPL SOP context.
3. If the user asks a greeting, math, general science, or coding question, answer naturally, helpfully, and authoritatively.

--- Context from Searchable Standards & Manuals Knowledge Base ---
{context}

--- Conversation History ---
{history}

User Question: {query}

PRAHARI AI Response:"""


# ── Helper Functions ───────────────────────────────────────────────────────────

def is_ollama_available(timeout_sec: float = 0.8) -> bool:
    """Check if the local Ollama server is responsive."""
    try:
        with httpx.Client(timeout=timeout_sec) as client:
            resp = client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            return resp.status_code == 200
    except Exception:
        return False


def _get_llm(temperature: float = 0.1) -> ChatOllama:
    return ChatOllama(
        model=settings.LLM_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=temperature,
        num_ctx=2048,
    )


def _format_context(docs: List[Document]) -> str:
    if not docs:
        return "No specific manual chunks retrieved."
    parts = []
    for i, doc in enumerate(docs, 1):
        filename = doc.metadata.get("filename", os.path.basename(doc.metadata.get("source", "MRPL_SOP")))
        page = doc.metadata.get("page", 1)
        content = doc.page_content.strip()
        parts.append(f"[Document {i}: {filename} | Section/Page {page}]\n{content}")
    return "\n\n".join(parts)


def _format_history(history: Optional[List[Dict]]) -> str:
    if not history:
        return "None"
    formatted = []
    for msg in history[-4:]:
        role = "Operator" if msg.get("role") == "user" else "PRAHARI AI"
        formatted.append(f"{role}: {msg.get('content', '')}")
    return "\n".join(formatted)


def _extract_citations(docs: List[Document]) -> List[Dict[str, Any]]:
    citations = []
    seen = set()
    for doc in docs:
        filename = doc.metadata.get("filename", os.path.basename(doc.metadata.get("source", "MRPL_SOP")))
        page = doc.metadata.get("page", 1)
        key = f"{filename}:{page}"
        if key not in seen:
            seen.add(key)
            snippet = doc.page_content.strip()[:200] + "..."
            citations.append({
                "document": filename,
                "page": page,
                "filepath": doc.metadata.get("filepath", doc.metadata.get("source", "")),
                "snippet": snippet,
            })
    return citations


# ── Core Hybrid RAG Pipeline ──────────────────────────────────────────────────

def query_rag_engine(
    query: str,
    session_history: Optional[List[Dict]] = None,
    document_filter: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main Universal Hybrid Pipeline (Online Cloud AI + Offline Neural Failover):
      1. Check internet connectivity.
      2. If online:
         - Live Web Search (BIS notifications, QCOs, real-time standards)
         - If Gemini configured: run Gemini 1.5/2.0 Flash
         - If Ollama running: run Ollama augmented with real-time web context
         - Else: synthesize live web search with standards database
      3. If offline (or online times out):
         - Hybrid Dense Vector + BM25Okapi local retrieval
         - If Ollama running: run local Ollama neural model (llama3.2)
         - Else: run Sovereign Offline Intelligence Engine (resilient air-gapped)
    """
    t_start = time.time()
    trace = []

    # 1. Local Hybrid Retrieval (Always available from SQLite/ChromaDB)
    docs = []
    try:
        docs = hybrid_retrieve(query, document_filter=document_filter)
        trace.append({"step": "hybrid_retrieval", "docs_found": len(docs), "bm25_weight": settings.BM25_WEIGHT})
    except Exception as e:
        trace.append({"step": "hybrid_retrieval", "error": str(e)})

    # 2. Check Internet Connectivity for Online Mode
    has_internet = is_internet_connected(timeout=0.8)
    trace.append({"step": "network_status", "is_online": has_internet})

    if has_internet:
        context = _format_context(docs)
        history_str = _format_history(session_history)

        # A. Live Web Search for up-to-the-minute updates
        web_snippets = search_live_web(query, max_results=4)
        if web_snippets:
            trace.append({"step": "live_web_search", "snippets_found": len(web_snippets)})

        # B. Try Cloud Generative AI (Gemini 1.5/2.0)
        cloud_answer = call_gemini_cloud_llm(query, context, web_snippets, history_str)
        if cloud_answer:
            trace.append({"step": "answer_generation", "mode": "Google Gemini (Cloud Neural AI)"})
            citations = _extract_citations(docs) if docs else []
            for w in web_snippets[:3]:
                citations.append({
                    "document": w.get("url", "Web"),
                    "page": 1,
                    "snippet": w.get("snippet", "")[:200] + "...",
                    "standard": w.get("title", "")[:40],
                    "clause": "Live Web Source",
                })
            return {
                "query": query,
                "rewritten_query": query,
                "answer": cloud_answer,
                "citations": citations,
                "model": "Gemini 1.5 Flash (Online Cloud AI)",
                "mode": "Online Cloud Neural AI",
                "hops": 1,
                "latency_ms": int((time.time() - t_start) * 1000),
                "execution_trace": trace,
            }

        # C. If Ollama is available, augment Ollama with live web data
        if is_ollama_available():
            try:
                llm = _get_llm()
                aug_context = context
                if web_snippets:
                    aug_context += "\n\n--- Live Web Updates ---\n" + "\n".join(
                        [f"- [{w['title']}]: {w['snippet']}" for w in web_snippets]
                    )
                prompt = ChatPromptTemplate.from_template(ANSWER_PROMPT)
                chain = prompt | llm
                result = chain.invoke({"context": aug_context, "query": query, "history": history_str})
                answer_text = result.content.strip()
                trace.append({"step": "answer_generation", "mode": f"Online Web-Augmented Ollama ({settings.LLM_MODEL})"})

                citations = _extract_citations(docs) if docs else []
                for w in web_snippets[:3]:
                    citations.append({
                        "document": w.get("url", "Web"),
                        "page": 1,
                        "snippet": w.get("snippet", "")[:200] + "...",
                        "standard": w.get("title", "")[:40],
                        "clause": "Live Web Source",
                    })
                return {
                    "query": query,
                    "rewritten_query": query,
                    "answer": answer_text,
                    "citations": citations,
                    "model": f"{settings.LLM_MODEL} (Web-Augmented)",
                    "mode": f"Online Web-Augmented LLM ({settings.LLM_MODEL})",
                    "hops": 1,
                    "latency_ms": int((time.time() - t_start) * 1000),
                    "execution_trace": trace,
                }
            except Exception as err:
                trace.append({"step": "online_ollama_fallback", "error": str(err)})

        # D. Online Web Synthesis fallback
        if web_snippets:
            online_res = synthesize_online_response(query, docs, web_snippets)
            trace.append({"step": "answer_generation", "mode": "Online Live Web Intelligence"})
            citations = online_res["citations"] + (_extract_citations(docs) if docs else [])
            return {
                "query": query,
                "rewritten_query": query,
                "answer": online_res["answer"],
                "citations": citations,
                "model": "Live Web Synthesis Engine",
                "mode": "Online Live Web Intelligence",
                "hops": 1,
                "latency_ms": int((time.time() - t_start) * 1000),
                "execution_trace": trace,
            }

    # 3. Offline Mode (When device has NO internet or internet check timed out)
    trace.append({"step": "offline_mode_active", "reason": "No internet connection or air-gapped mode"})
    ollama_ready = is_ollama_available()

    if ollama_ready:
        context = _format_context(docs)
        history_str = _format_history(session_history)
        try:
            llm = _get_llm()
            prompt = ChatPromptTemplate.from_template(ANSWER_PROMPT)
            chain = prompt | llm
            result = chain.invoke({
                "context": context,
                "query": query,
                "history": history_str,
            })
            answer_text = result.content.strip()
            trace.append({"step": "answer_generation", "mode": f"Local Offline Neural LLM ({settings.LLM_MODEL})"})

            citations = _extract_citations(docs) if docs else []
            return {
                "query": query,
                "rewritten_query": query,
                "answer": answer_text,
                "citations": citations,
                "model": settings.LLM_MODEL,
                "mode": f"Offline Neural LLM ({settings.LLM_MODEL})",
                "hops": 1,
                "latency_ms": int((time.time() - t_start) * 1000),
                "execution_trace": trace,
            }
        except Exception as err:
            trace.append({"step": "llm_fallback_to_offline_engine", "error": str(err)})

    # 4. Sovereign Offline Extractive Safety Engine (100% reliable fallback)
    res = offline_intelligence.answer_query(query, docs=docs, history=session_history)
    trace.append({"step": "answer_generation", "mode": res.get("mode", "Sovereign Offline Intelligence")})

    latency_ms = int((time.time() - t_start) * 1000)
    return {
        "query": query,
        "rewritten_query": query,
        "answer": res["answer"],
        "citations": res.get("citations", []),
        "follow_up_options": res.get("follow_up_options", []),
        "intent": res.get("intent", ""),
        "model": "Sovereign Offline Intelligence Engine",
        "mode": res.get("mode", "100% Offline Air-Gapped"),
        "hops": 1 if docs else 0,
        "latency_ms": latency_ms,
        "execution_trace": trace,
    }


async def stream_rag_response(
    query: str,
    session_history: Optional[List[Dict]] = None,
    document_filter: Optional[str] = None,
) -> AsyncGenerator[str, None]:
    """
    Async generator that yields SSE-compatible token chunks in real-time.
    Supports both local Ollama streaming and sovereign offline token streaming.
    """
    import json as _json

    t_start = time.time()

    yield f"data: {_json.dumps({'type': 'rewrite', 'rewritten_query': query})}\n\n"

    # Step 1: Hybrid Retrieval
    docs = []
    try:
        docs = hybrid_retrieve(query, document_filter=document_filter)
    except Exception:
        docs = []

    yield f"data: {_json.dumps({'type': 'retrieval', 'docs_found': len(docs)})}\n\n"

    ollama_ready = is_ollama_available()

    if ollama_ready:
        context = _format_context(docs)
        history_str = _format_history(session_history)

        try:
            llm = _get_llm()
            prompt = ChatPromptTemplate.from_template(ANSWER_PROMPT)
            chain = prompt | llm

            full_text = ""
            async for chunk in chain.astream({
                "context": context,
                "query": query,
                "history": history_str,
            }):
                token = chunk.content
                full_text += token
                yield f"data: {_json.dumps({'type': 'token', 'text': token})}\n\n"

            citations = _extract_citations(docs) if docs else []
            latency_ms = int((time.time() - t_start) * 1000)
            yield f"data: {_json.dumps({'type': 'done', 'rewritten_query': query, 'citations': citations, 'model': settings.LLM_MODEL, 'latency_ms': latency_ms})}\n\n"
            return
        except Exception:
            pass

    # Sovereign Offline Streaming
    offline_res = offline_intelligence.answer_query(query, docs=docs, history=session_history)
    answer_text = offline_res["answer"]
    citations = offline_res.get("citations", [])
    follow_up_options = offline_res.get("follow_up_options", [])
    intent = offline_res.get("intent", "")
    model_name = offline_res.get("mode", "Sovereign Offline Intelligence Engine")

    # Stream text in small rhythmic token chunks for a smooth real-time visual experience
    words = re.split(r'(\s+)', answer_text)
    for i in range(0, len(words), 2):
        chunk = "".join(words[i:i+2])
        yield f"data: {_json.dumps({'type': 'token', 'text': chunk})}\n\n"
        await asyncio.sleep(0.012)

    latency_ms = int((time.time() - t_start) * 1000)
    yield f"data: {_json.dumps({'type': 'done', 'rewritten_query': query, 'citations': citations, 'follow_up_options': follow_up_options, 'intent': intent, 'model': model_name, 'latency_ms': latency_ms})}\n\n"
