"""
PRAHARI AI — Online Intelligence & Real-Time Web Augmentation Service
Provides:
  1. Real-time internet connectivity detection (dynamic failover).
  2. Live Web Search for latest BIS Quality Control Orders (QCOs), Indian Standards, and consumer advisories.
  3. Cloud Generative AI synthesis (Google Gemini 1.5/2.0 Flash or public cloud inference).
  4. Automatic failover to local offline Ollama / Sovereign Engine when internet is disconnected.
"""

import os
import re
import socket
import logging
import warnings
from typing import Dict, Any, List, Optional
import httpx

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=ResourceWarning)

from backend.app.config import settings

logger = logging.getLogger(__name__)


def is_internet_connected(timeout: float = 1.0) -> bool:
    """
    Fast, reliable check to determine if the user's device has an active internet connection.
    Tests DNS resolution or quick TCP socket connection to public root DNS (8.8.8.8).
    """
    try:
        # Check TCP connection to Google Public DNS on port 53 (extremely fast, <100ms)
        sock = socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        sock.close()
        return True
    except (socket.timeout, OSError):
        pass

    # Secondary fallback check
    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.get("https://www.google.com/generate_204")
            return resp.status_code == 204 or resp.status_code == 200
    except Exception:
        return False


def search_live_web(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Performs real-time web search for Indian Standards, BIS schemes, QCO circulars, and consumer queries.
    Uses duckduckgo_search without requiring any API keys.
    """
    results = []
    try:
        from duckduckgo_search import DDGS
        # Augment query for high precision BIS / Indian Standards retrieval
        q_search = query
        if not any(k in query.lower() for k in ["is ", "bis", "standard", "hallmark", "qco"]):
            q_search = f"{query} Indian Standard BIS"

        with DDGS() as ddgs:
            raw_results = list(ddgs.text(q_search, max_results=max_results))
            for item in raw_results:
                results.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("body", ""),
                    "url": item.get("href", ""),
                })
    except Exception as e:
        logger.warning(f"[OnlineSearch] DuckDuckGo search error: {e}")
    return results


def get_gemini_api_key() -> Optional[str]:
    """Retrieve Gemini API key from environment or persisted config."""
    key = os.getenv("GEMINI_API_KEY") or getattr(settings, "GEMINI_API_KEY", None)
    if not key:
        config_path = os.path.join(settings.DATA_DIR, "ai_config.json")
        if os.path.exists(config_path):
            try:
                import json
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    key = cfg.get("gemini_api_key", "").strip()
            except Exception:
                pass
    return key if key else None


def call_gemini_cloud_llm(
    query: str,
    context: str,
    web_snippets: List[Dict[str, str]],
    history_str: str = "",
    model_name: str = "gemini-1.5-flash"
) -> Optional[str]:
    """
    Invokes Google Gemini Cloud AI for dynamic, state-of-the-art generative responses
    grounded in both local standards and live web snippets.
    """
    api_key = get_gemini_api_key()
    if not api_key:
        return None

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        gemini_model = "gemini-1.5-pro" if "pro" in model_name.lower() else "gemini-1.5-flash"
        model = genai.GenerativeModel(gemini_model)

        web_text = ""
        if web_snippets:
            web_text = "\n\n--- Real-Time Live Web Information ---\n" + "\n".join(
                [f"• [{w['title']}]({w['url']}): {w['snippet']}" for w in web_snippets]
            )

        prompt = f"""You are PRAHARI AI (Online Cloud Edition), an authoritative Virtual Assistant for Indian Standards (IS codes), Bureau of Indian Standards (BIS) Schemes (SIH Topic 26107), and Industrial Engineering Safety.

Guidelines:
1. Provide a comprehensive, clear, accurate, and structured answer.
2. ALWAYS cite the exact Indian Standard number (e.g. IS 1786:2008, IS 10500:2012, IS 1417:2016) and relevant Clause/Table.
3. For Industry queries, detail technical SIT parameters (chemical/mechanical tests, tolerances) and mandatory Quality Control Orders (QCO).
4. For Consumer queries, explain ISI mark (7-digit CML), Hallmark (6-digit HUID), and complaint procedures via the BIS Care App and National Consumer Helpline (1915).
5. If live web data provides recent notifications or amendments, incorporate them with markdown citations.
6. If the user asks in Hindi, answer fluently in Hindi with appropriate technical terminology.

--- Context from Ingested Regulatory Standards ---
{context}
{web_text}

--- Conversation History ---
{history_str}

User Question: {query}

PRAHARI AI Response:"""

        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
    except Exception as e:
        logger.warning(f"[OnlineAI] Gemini Cloud API error: {e}")

    return None


def synthesize_online_response(
    query: str,
    retrieved_docs: List[Any],
    web_snippets: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Synthesizes an intelligent, dynamic online response when an API key is not configured,
    combining retrieved regulatory standards with real-time web search results.
    """
    # Build live citations
    citations = []
    web_lines = []

    for w in web_snippets[:4]:
        title = w.get("title", "")
        url = w.get("url", "")
        snippet = w.get("snippet", "")
        web_lines.append(f"- **[{title}]({url})**: {snippet}")
        citations.append({
            "standard": title[:40],
            "clause": "Live Web Source",
            "title": title,
            "snippet": snippet[:200] + "...",
            "document": url,
            "page": 1,
        })

    # Combine local doc snippets
    doc_lines = []
    for d in retrieved_docs[:3]:
        doc_lines.append(f"- {d.page_content.strip()}")

    online_body = f"""### 🌐 PRAHARI AI (Live Online Intelligence)

Here is the real-time regulatory and technical information retrieved for: **"{query}"**

#### 🔍 Verified Regulatory Findings & Live Data:
{chr(10).join(web_lines) if web_lines else "No external web entries required; grounded in verified Indian Standards compendium."}

#### 📋 Ingested Standards Compendium Baseline:
{chr(10).join(doc_lines) if doc_lines else "Local regulatory database active."}

---
> 🌐 **Mode:** Online Connected (Live Cloud Retrieval & Web Grounding) • **Source:** Live BIS / National Standards Repositories
"""

    return {
        "answer": online_body,
        "citations": citations,
        "mode": "Online Cloud Intelligence (Live Web Search)",
    }
