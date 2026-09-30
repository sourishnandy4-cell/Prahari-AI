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

ENGLISH_ANSWER_PROMPT = """You are PRAHARI AI, the authoritative Virtual Assistant for Indian Standards (IS codes), Bureau of Indian Standards (BIS) Schemes (SIH Topic 26107), and Industrial Engineering & Operational Safety.

CRITICAL MANDATORY INSTRUCTION:
Your ENTIRE response MUST be in 100% English.
DO NOT use Thai, Chinese, Hindi, Devanagari script, or any non-English language under any circumstances. Every single word must be in standard English.

Guidelines:
1. Provide a well-structured, clear, concise, and accurate answer in English. Never loop or repeat phrases.
2. For Indian Standards (IS codes) & BIS schemes:
   - State the exact Standard Number (e.g. IS 10500:2012, IS 4151:2015, IS 1293:2019, IS 1786:2008) and relevant requirements.
   - For industry queries, describe technical testing (impact, penetration, retention) and mandatory Quality Control Orders (QCO).
   - For consumer queries, explain ISI mark (7-digit CML), Hallmark (6-digit HUID), and complaint lodging via BIS Care App or Helpline (1800-11-1255 / 1915).
3. If the question relates to industrial safety or MRPL refinery SOPs, strictly ground your response in the provided context.
4. If the answer is not in the context, guide the user to the BIS website (www.bis.gov.in) or Toll-Free Helpline (1800-11-1255).

--- Context from Knowledge Base ---
{context}

--- Conversation History ---
{history}

User Question: {query}

PRAHARI AI Response (in 100% English only):"""

HINDI_ANSWER_PROMPT = """आप प्रहरी एआई (PRAHARI AI) हैं, जो भारतीय मानक (IS कोड), भारतीय मानक ब्यूरो (BIS) योजनाओं (SIH विषय 26107) और औद्योगिक एवं परिचालन सुरक्षा के लिए आधिकारिक वर्चुअल सहायक हैं।

अत्यंत महत्वपूर्ण अनिवार्य निर्देश:
आपका संपूर्ण उत्तर 100% केवल हिन्दी (देवनागरी लिपि) में होना चाहिए। किसी भी विदेशी या अन्य भाषा का प्रयोग कदापि न करें।

दिशानिर्देश:
1. स्पष्ट, संरचित, संक्षिप्त एवं सटीक हिन्दी में उत्तर दें।
2. भारतीय मानक (IS Codes) और बीआईएस योजनाओं के लिए:
   - सटीक मानक संख्या (जैसे IS 10500:2012, IS 4151:2015, IS 1293:2019, IS 1786:2008) का स्पष्ट उल्लेख करें।
   - उद्योगों के लिए अनिवार्य प्रयोगशाला परीक्षण और गुणवत्ता नियंत्रण आदेश (QCO) की जानकारी दें।
   - उपभोक्ताओं के लिए असली आईएसआई मार्क (7-अंकीय CML), हॉलमार्क (6-अंकीय HUID) और बीआईएस केयर ऐप या हेल्पलाइन (1800-11-1255 / 1915) पर शिकायत दर्ज करने की विधि समझाएं।
3. यदि जानकारी संदर्भ में उपलब्ध न हो, तो उपयोगकर्ता को बीआईएस की आधिकारिक वेबसाइट (www.bis.gov.in) या राष्ट्रीय टोल-फ्री हेल्पलाइन (1800-11-1255) से संपर्क करने का निर्देश दें।

--- ज्ञानकोष संदर्भ (Context) ---
{context}

--- पूर्व बातचीत ---
{history}

उपयोगकर्ता का प्रश्न: {query}

प्रहरी एआई उत्तर (केवल हिन्दी में):"""

ANSWER_PROMPT = ENGLISH_ANSWER_PROMPT


# ── Helper Functions ───────────────────────────────────────────────────────────

def is_conversational_query(query: str) -> bool:
    """Detects simple conversational greetings, identity questions, or expressions of thanks."""
    q_low = query.strip().lower()
    cleaned = re.sub(r'[^\w\s]', '', q_low).strip()
    words = cleaned.split()
    if not words:
        return True

    greetings = {
        "hi", "hello", "hey", "hola", "namaste", "namaskar", "howdy",
        "sup", "yo", "hlo", "helo", "good morning", "good afternoon",
        "good evening", "good day", "greetings",
        "नमस्ते", "प्रणाम", "नमस्कार", "हेलो", "हाय"
    }
    if cleaned in greetings:
        return True
    if words and words[0] in greetings and len(words) <= 5:
        return True

    phrases = [
        "who are you", "what is your name", "what are you", "what can you do",
        "tell me about yourself", "how are you", "how r u", "who made you",
        "help me", "help", "what is prahari", "what is bis",
        "thank you", "thanks", "thanks a lot", "bye", "goodbye", "see you",
        "तुम कौन हो", "आप कौन हैं", "तुम्हारा नाम क्या है", "धन्यवाद", "शुक्रिया"
    ]
    if any(cleaned == p or cleaned.startswith(p) for p in phrases):
        return True
    return False


def contains_foreign_script(text: str, target_language: str) -> bool:
    """
    Checks if text contains unauthorized foreign scripts.
    - Thai script: \u0E00 to \u0E7F
    - Chinese/CJK characters: \u4E00 to \u9FFF, \u3040 to \u30FF
    - Arabic script: \u0600 to \u06FF
    - For English: checks for Devanagari (\u0900-\u097F) leaking into English responses.
    """
    thai_count = sum(1 for c in text if '\u0E00' <= c <= '\u0E7F')
    if thai_count > 0:
        return True

    cjk_count = sum(1 for c in text if '\u4E00' <= c <= '\u9FFF' or '\u3040' <= c <= '\u30FF')
    if cjk_count > 0:
        return True

    arabic_count = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
    if arabic_count > 0:
        return True

    if target_language == "English":
        dev_count = sum(1 for c in text if '\u0900' <= c <= '\u097F')
        if dev_count > 2:
            return True

    return False


def _detect_language(query: str, user_language: Optional[str] = None):
    """Detect language preference: explicit user_language takes absolute priority."""
    if user_language == "hi":
        return "Hindi", "Respond ENTIRELY in Hindi (Devanagari script). Do NOT use English in your response."
    if user_language == "en":
        return "English", "Respond ENTIRELY in English. Do NOT use Hindi, Thai, or any foreign language."

    devanagari_chars = sum(1 for c in query if '\u0900' <= c <= '\u097F')
    if devanagari_chars > 2 or (devanagari_chars / max(len(query), 1)) > 0.3:
        return "Hindi", "Respond ENTIRELY in Hindi (Devanagari script). Do NOT use English in your response."
    return "English", "Respond ENTIRELY in English. Do NOT use Hindi, Thai, or any foreign language."

def is_ollama_available(timeout_sec: float = 0.8) -> bool:
    """Check if the local Ollama server is responsive."""
    try:
        with httpx.Client(timeout=timeout_sec) as client:
            resp = client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            return resp.status_code == 200
    except Exception:
        return False


def _get_llm(temperature: float = 0.3) -> ChatOllama:
    return ChatOllama(
        model=settings.LLM_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=temperature,
        repeat_penalty=1.2,
        top_p=0.9,
        num_ctx=2048,
    )


def _format_context(docs: List[Document], target_language: str = "English") -> str:
    if not docs:
        return "No specific manual chunks retrieved."
    parts = []
    for i, doc in enumerate(docs, 1):
        filename = doc.metadata.get("filename", os.path.basename(doc.metadata.get("source", "MRPL_SOP")))
        page = doc.metadata.get("page", 1)
        content = doc.page_content.strip()
        if target_language == "English":
            # Filter out Hindi lines (Devanagari) to prevent LLaMA 3.2 from inadvertently switching languages
            clean_lines = []
            for line in content.split("\n"):
                dev_count = sum(1 for c in line if '\u0900' <= c <= '\u097F')
                if dev_count > 4 and dev_count / max(len(line), 1) > 0.2:
                    continue
                clean_lines.append(line)
            content = "\n".join(clean_lines).strip()
        parts.append(f"[Document {i}: {filename} | Section/Page {page}]\n{content}")
    return "\n\n".join(parts)


def _format_history(history: Optional[List[Dict]], target_language: str = "English") -> str:
    if not history:
        return "None"
    formatted = []
    for msg in history[-4:]:
        role = "Operator" if msg.get("role") == "user" else "PRAHARI AI"
        content = msg.get('content', '')
        if target_language == "English" and role == "PRAHARI AI":
            # Sanitize Hindi out of history to prevent model from imitating previous Hindi turns
            dev_count = sum(1 for c in content if '\u0900' <= c <= '\u097F')
            if dev_count > 5 and (dev_count / max(len(content), 1)) > 0.25:
                content = "[Previous answer provided in Hindi]"
        formatted.append(f"{role}: {content}")
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


def get_persisted_ai_config() -> Dict[str, Any]:
    """Reads persisted AI configuration (active model & key) from data/ai_config.json."""
    config_path = os.path.join(settings.DATA_DIR, "ai_config.json")
    if os.path.exists(config_path):
        try:
            import json
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "active_model": "llama3.2-web",
        "gemini_api_key": os.getenv("GEMINI_API_KEY", "")
    }


# ── Core Hybrid RAG Pipeline ──────────────────────────────────────────────────

def query_rag_engine(
    query: str,
    session_history: Optional[List[Dict]] = None,
    document_filter: Optional[str] = None,
    user_language: Optional[str] = "en",
) -> Dict[str, Any]:
    """
    Universal Hybrid Pipeline (Online Cloud Gemini / LLaMA 3.2 Web + Offline Local Failover):
      1. Fast path for conversational greetings and small talk (0 ms latency, no retrieval).
      2. Reads active_model preference from user settings (gemini-1.5-flash, gemini-1.5-pro, llama3.2-web, llama3.2-offline).
      3. If offline model requested, immediately routes to local neural engine.
      4. If online requested, checks internet connectivity:
         - Fetches live web updates (BIS QCOs, Gazette notifications).
         - If Gemini selected & key present -> runs Google Gemini 1.5 Flash/Pro.
         - If LLaMA 3.2 Web selected -> runs local LLaMA 3.2 augmented with live web data.
      5. Strict language enforcement: English query -> 100% English, Hindi query -> 100% Hindi.
      6. Automatic foreign script detection and fallback to sovereign offline intelligence.
    """
    t_start = time.time()
    trace = []

    # Conversational Fast Path (Greetings, small talk, identity)
    if is_conversational_query(query):
        conv_res = offline_intelligence.answer_query(query, docs=[], history=session_history, user_language=user_language)
        return {
            "query": query,
            "rewritten_query": query,
            "answer": conv_res["answer"],
            "citations": [],
            "model": "PRAHARI Conversational Engine",
            "mode": "Conversational Greeting",
            "hops": 0,
            "latency_ms": int((time.time() - t_start) * 1000),
            "execution_trace": [{"step": "conversational_fast_path", "intent": "greeting"}],
        }

    ai_cfg = get_persisted_ai_config()
    active_model = ai_cfg.get("active_model", "llama3.2-web")

    lang_name, lang_instruction = _detect_language(query, user_language=user_language)

    # 1. Local Hybrid Retrieval (Always available from SQLite/ChromaDB)
    docs = []
    try:
        docs = hybrid_retrieve(query, document_filter=document_filter)
        trace.append({"step": "hybrid_retrieval", "docs_found": len(docs), "bm25_weight": settings.BM25_WEIGHT})
    except Exception as e:
        trace.append({"step": "hybrid_retrieval", "error": str(e)})

    # 2. Check if user explicitly forced 100% Offline Mode
    if active_model == "llama3.2-offline":
        trace.append({"step": "user_preference", "mode": "Forced 100% Offline Air-Gapped"})
        has_internet = False
    else:
        # Check Internet Connectivity
        has_internet = is_internet_connected(timeout=0.8)
        trace.append({"step": "network_status", "is_online": has_internet, "active_model": active_model})

    if has_internet:
        context = _format_context(docs, target_language=lang_name)
        history_str = _format_history(session_history, target_language=lang_name)

        # A. Live Web Search for up-to-the-minute updates
        web_snippets = search_live_web(query, max_results=4)
        if web_snippets:
            trace.append({"step": "live_web_search", "snippets_found": len(web_snippets)})

        # B. If user chose Gemini (or default) and has a key
        if active_model.startswith("gemini"):
            cloud_answer = call_gemini_cloud_llm(query, context, web_snippets, history_str, model_name=active_model, user_language=user_language)
            if cloud_answer:
                # Sanitize if foreign script detected
                if contains_foreign_script(cloud_answer, target_language=lang_name):
                    offline_res = offline_intelligence.answer_query(query, docs=docs, history=session_history, user_language=user_language)
                    cloud_answer = offline_res["answer"]
                model_label = "Google Gemini 1.5 Pro" if "pro" in active_model else "Google Gemini 1.5 Flash"
                trace.append({"step": "answer_generation", "mode": f"{model_label} (Cloud Neural AI)"})
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
                    "model": f"{model_label} (Live Online)",
                    "mode": "Online Cloud Neural AI",
                    "hops": 1,
                    "latency_ms": int((time.time() - t_start) * 1000),
                    "execution_trace": trace,
                }
            else:
                trace.append({"step": "gemini_unavailable", "reason": "No API key or quota issue. Falling back to local neural engine."})

        # C. If LLaMA 3.2 + Web (or Gemini fallback) and Ollama is available
        if is_ollama_available():
            try:
                llm = _get_llm()
                aug_context = context
                if web_snippets:
                    aug_context += "\n\n--- Live Web Updates ---\n" + "\n".join(
                        [f"- [{w['title']}]: {w['snippet']}" for w in web_snippets]
                    )
                prompt_tpl = HINDI_ANSWER_PROMPT if lang_name == "Hindi" else ENGLISH_ANSWER_PROMPT
                prompt = ChatPromptTemplate.from_template(prompt_tpl)
                chain = prompt | llm
                result = chain.invoke({"context": aug_context, "query": query, "history": history_str})
                answer_text = result.content.strip()

                # Sanitize if foreign script detected
                if contains_foreign_script(answer_text, target_language=lang_name):
                    offline_res = offline_intelligence.answer_query(query, docs=docs, history=session_history, user_language=user_language)
                    answer_text = offline_res["answer"]

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

    # 3. Offline Mode (When device has NO internet, user picked offline, or external API failed)
    trace.append({"step": "offline_mode_active", "reason": "No internet connection or air-gapped mode"})
    ollama_ready = is_ollama_available()

    if ollama_ready:
        context = _format_context(docs, target_language=lang_name)
        history_str = _format_history(session_history, target_language=lang_name)
        try:
            llm = _get_llm()
            prompt_tpl = HINDI_ANSWER_PROMPT if lang_name == "Hindi" else ENGLISH_ANSWER_PROMPT
            prompt = ChatPromptTemplate.from_template(prompt_tpl)
            chain = prompt | llm
            result = chain.invoke({
                "context": context,
                "query": query,
                "history": history_str,
            })
            answer_text = result.content.strip()

            if contains_foreign_script(answer_text, target_language=lang_name):
                offline_res = offline_intelligence.answer_query(query, docs=docs, history=session_history, user_language=user_language)
                answer_text = offline_res["answer"]

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
    res = offline_intelligence.answer_query(query, docs=docs, history=session_history, user_language=user_language)
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
    user_language: Optional[str] = "en",
) -> AsyncGenerator[str, None]:
    """
    Async generator that yields SSE-compatible token chunks in real-time.
    Supports conversational fast path, local Ollama streaming with foreign script guardrails,
    and sovereign offline token streaming.
    """
    import json as _json

    t_start = time.time()

    yield f"data: {_json.dumps({'type': 'rewrite', 'rewritten_query': query})}\n\n"

    # Conversational Fast Path (Greetings, small talk, identity)
    if is_conversational_query(query):
        yield f"data: {_json.dumps({'type': 'retrieval', 'docs_found': 0})}\n\n"
        conv_res = offline_intelligence.answer_query(query, docs=[], history=session_history, user_language=user_language)
        answer_text = conv_res["answer"]
        words = re.split(r'(\s+)', answer_text)
        for i in range(0, len(words), 2):
            chunk = "".join(words[i:i+2])
            yield f"data: {_json.dumps({'type': 'token', 'text': chunk})}\n\n"
            await asyncio.sleep(0.012)
        latency_ms = int((time.time() - t_start) * 1000)
        yield f"data: {_json.dumps({'type': 'done', 'rewritten_query': query, 'citations': [], 'model': 'PRAHARI Conversational Engine', 'latency_ms': latency_ms})}\n\n"
        return

    # Step 1: Hybrid Retrieval
    docs = []
    try:
        docs = hybrid_retrieve(query, document_filter=document_filter)
    except Exception:
        docs = []

    yield f"data: {_json.dumps({'type': 'retrieval', 'docs_found': len(docs)})}\n\n"

    lang_name, lang_instruction = _detect_language(query, user_language=user_language)
    context = _format_context(docs, target_language=lang_name)
    history_str = _format_history(session_history, target_language=lang_name)

    ai_cfg = get_persisted_ai_config()
    active_model = ai_cfg.get("active_model", "llama3.2-web")
    gemini_key = ai_cfg.get("gemini_api_key") or os.getenv("GEMINI_API_KEY", "")

    # Mode 1: Google Gemini Streaming (when Gemini is active or configured)
    if gemini_key and ("gemini" in active_model.lower() or not is_ollama_available()):
        try:
            import queue
            import threading
            from google import genai

            client = genai.Client(api_key=gemini_key)
            g_model = "models/gemini-1.5-pro" if "pro" in active_model.lower() else "models/gemini-1.5-flash"

            if lang_name == "Hindi":
                g_directive = "उत्तर केवल और केवल हिन्दी (देवनागरी लिपि) में दें।"
                g_lang_rule = "The user selected Hindi. You MUST write your ENTIRE response in Hindi (Devanagari script) ONLY. Do not use English."
            else:
                g_directive = "Respond ENTIRELY in English. Do NOT use Thai, Hindi, or any foreign language."
                g_lang_rule = "The user selected English. You MUST write your ENTIRE response in English ONLY. Do not use Hindi, Thai, or any foreign language."

            prompt = f"""CRITICAL LANGUAGE DIRECTIVE — MANDATORY:
{g_lang_rule} {g_directive}

You are PRAHARI AI (Online Cloud Edition), an authoritative Virtual Assistant for Indian Standards (IS codes), Bureau of Indian Standards (BIS) Schemes (SIH Topic 26107), and Industrial Engineering Safety.

Guidelines:
1. Always respond strictly in {lang_name}.
2. Provide a comprehensive, clear, accurate, and structured answer. Never loop or repeat phrases.
3. ALWAYS cite the exact Indian Standard number (e.g. IS 1786:2008, IS 10500:2012, IS 1417:2016) and relevant Clause/Table.
4. For Industry queries, detail technical SIT parameters (chemical/mechanical tests, tolerances) and mandatory Quality Control Orders (QCO).
5. For Consumer queries, explain ISI mark (7-digit CML), Hallmark (6-digit HUID), and complaint procedures via the BIS Care App and National Consumer Helpline (1915).

--- Context from Ingested Regulatory Standards ---
{context}

--- Conversation History ---
{history_str}

User Question: {query}

PRAHARI AI Response (in {lang_name} only):"""

            token_queue = queue.Queue()

            def _stream_worker():
                try:
                    stream_res = client.models.generate_content_stream(model=g_model, contents=prompt)
                    for chunk in stream_res:
                        txt = getattr(chunk, 'text', None)
                        if txt:
                            token_queue.put(("token", txt))
                    token_queue.put(("end", None))
                except Exception as stream_err:
                    token_queue.put(("error", str(stream_err)))

            worker_thread = threading.Thread(target=_stream_worker, daemon=True)
            worker_thread.start()

            gemini_streamed_any = False
            full_gemini_text = ""
            corrupt_gemini = False
            while True:
                try:
                    msg_type, val = token_queue.get_nowait()
                    if msg_type == "token":
                        full_gemini_text += val
                        if contains_foreign_script(full_gemini_text, target_language=lang_name):
                            corrupt_gemini = True
                            break
                        gemini_streamed_any = True
                        yield f"data: {_json.dumps({'type': 'token', 'text': val})}\n\n"
                    elif msg_type == "end":
                        break
                    elif msg_type == "error":
                        if not gemini_streamed_any:
                            raise Exception(val)
                        break
                except queue.Empty:
                    if not worker_thread.is_alive() and token_queue.empty():
                        break
                    await asyncio.sleep(0.015)

            if gemini_streamed_any and not corrupt_gemini:
                citations = _extract_citations(docs) if docs else []
                latency_ms = int((time.time() - t_start) * 1000)
                model_label = "Google Gemini 1.5 Pro" if "pro" in active_model.lower() else "Google Gemini 1.5 Flash"
                yield f"data: {_json.dumps({'type': 'done', 'rewritten_query': query, 'citations': citations, 'model': model_label, 'latency_ms': latency_ms})}\n\n"
                return
        except Exception:
            pass

    # Mode 2: Local Ollama Neural LLM Streaming
    ollama_ready = is_ollama_available()
    if ollama_ready:
        try:
            llm = _get_llm()
            prompt_tpl = HINDI_ANSWER_PROMPT if lang_name == "Hindi" else ENGLISH_ANSWER_PROMPT
            prompt = ChatPromptTemplate.from_template(prompt_tpl)
            chain = prompt | llm

            full_text = ""
            corrupted = False
            async for chunk in chain.astream({
                "context": context,
                "query": query,
                "history": history_str,
            }):
                token = chunk.content
                full_text += token

                # If unauthorized script detected, break immediately!
                if contains_foreign_script(full_text, target_language=lang_name):
                    corrupted = True
                    break

                yield f"data: {_json.dumps({'type': 'token', 'text': token})}\n\n"

            if corrupted:
                # Do not leave user with corrupt / foreign text!
                # Fall back to sovereign offline intelligence clean answer
                offline_res = offline_intelligence.answer_query(query, docs=docs, history=session_history, user_language=user_language)
                clean_ans = offline_res["answer"]
                words = re.split(r'(\s+)', clean_ans)
                for i in range(0, len(words), 2):
                    chunk = "".join(words[i:i+2])
                    yield f"data: {_json.dumps({'type': 'token', 'text': chunk})}\n\n"
                    await asyncio.sleep(0.012)

                citations = _extract_citations(docs) if docs else []
                latency_ms = int((time.time() - t_start) * 1000)
                yield f"data: {_json.dumps({'type': 'done', 'rewritten_query': query, 'citations': citations, 'model': 'PRAHARI Guardrail Fallback', 'latency_ms': latency_ms})}\n\n"
                return

            citations = _extract_citations(docs) if docs else []
            latency_ms = int((time.time() - t_start) * 1000)
            yield f"data: {_json.dumps({'type': 'done', 'rewritten_query': query, 'citations': citations, 'model': settings.LLM_MODEL, 'latency_ms': latency_ms})}\n\n"
            return
        except Exception:
            pass

    # Mode 3: Sovereign Offline Intelligence Streaming
    offline_res = offline_intelligence.answer_query(query, docs=docs, history=session_history, user_language=user_language)
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
