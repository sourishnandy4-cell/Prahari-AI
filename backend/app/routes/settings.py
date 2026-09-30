"""
PRAHARI AI — AI Settings & Gemini Token Management Router
Provides:
  - GET  /api/settings/ai-config        -> Get active AI model, token status, network state
  - POST /api/settings/ai-config        -> Save active AI model and user Gemini API key
  - POST /api/settings/verify-gemini-token -> Verify user's token directly with Google Cloud
"""

import os
import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from backend.app.config import settings
from backend.app.services.online_ai_service import is_internet_connected
from backend.app.services.rag_service import is_ollama_available

router = APIRouter(prefix="/settings", tags=["AI Settings & Models"])

CONFIG_FILE = os.path.join(settings.DATA_DIR, "ai_config.json")


def _read_persisted_config() -> Dict[str, Any]:
    import json
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "active_model": "gemini-1.5-flash" if os.getenv("GEMINI_API_KEY") else "llama3.2-web",
        "gemini_api_key": os.getenv("GEMINI_API_KEY", "")
    }


def _write_persisted_config(data: Dict[str, Any]):
    import json
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


class AIConfigRequest(BaseModel):
    model: Optional[str] = None
    gemini_api_key: Optional[str] = None


class VerifyTokenRequest(BaseModel):
    gemini_api_key: str


@router.get("/ai-config")
async def get_ai_config():
    cfg = _read_persisted_config()
    gemini_key = cfg.get("gemini_api_key") or os.getenv("GEMINI_API_KEY", "")
    masked_key = None
    if gemini_key:
        masked_key = gemini_key[:7] + "..." + gemini_key[-4:] if len(gemini_key) > 12 else "****"

    online = is_internet_connected(timeout=0.8)
    ollama_ok = is_ollama_available()

    available_models = [
        {
            "id": "gemini-1.5-flash",
            "name": "Google Gemini 1.5 Flash",
            "provider": "Google Cloud AI",
            "type": "cloud",
            "badge": "⚡ Ultra-Fast Cloud AI",
            "description": "Google flagship fast multimodal model. 1M token context, sub-second responses. (Requires free Gemini Key)",
            "requires_key": True,
            "free_quota": "15 RPM, 1,500 requests/day free from Google"
        },
        {
            "id": "gemini-1.5-pro",
            "name": "Google Gemini 1.5 Pro",
            "provider": "Google Cloud AI",
            "type": "cloud",
            "badge": "🧠 Deep Reasoning Cloud AI",
            "description": "Google advanced reasoning model. Best for cross-referencing complex standards and QCOs.",
            "requires_key": True,
            "free_quota": "Available with free Google AI Studio token"
        },
        {
            "id": "llama3.2-web",
            "name": "Web-Augmented LLaMA 3.2",
            "provider": "Hybrid (Web + Local Neural)",
            "type": "hybrid",
            "badge": "🌐 Live Web Search + Neural AI",
            "description": "Searches the live internet for recent BIS announcements and passes them to local LLaMA 3.2. 100% Free.",
            "requires_key": False,
            "free_quota": "Unlimited & Free (No API key needed)"
        },
        {
            "id": "llama3.2-offline",
            "name": "Offline LLaMA 3.2",
            "provider": "Local Neural Engine",
            "type": "offline",
            "badge": "🔒 100% Air-Gapped",
            "description": "Runs entirely on your device with local ChromaDB vectorstore. Automatically activates if internet drops.",
            "requires_key": False,
            "free_quota": "Completely offline & sovereign"
        }
    ]

    return {
        "active_model": cfg.get("active_model", "llama3.2-web"),
        "gemini_configured": bool(gemini_key),
        "gemini_masked_key": masked_key,
        "is_online": online,
        "ollama_ready": ollama_ok,
        "get_key_url": "https://aistudio.google.com/app/apikey",
        "available_models": available_models,
    }


@router.post("/ai-config")
async def update_ai_config(req: AIConfigRequest):
    cfg = _read_persisted_config()

    if req.model:
        cfg["active_model"] = req.model

    if req.gemini_api_key is not None:
        key = req.gemini_api_key.strip()
        cfg["gemini_api_key"] = key
        # Also set in environment for active process
        if key:
            os.environ["GEMINI_API_KEY"] = key
            # If user added a Gemini key and hadn't picked a model, switch to gemini-1.5-flash
            if not req.model:
                cfg["active_model"] = "gemini-1.5-flash"
        else:
            os.environ.pop("GEMINI_API_KEY", None)

    _write_persisted_config(cfg)

    return {
        "status": "success",
        "message": f"Active AI model updated to '{cfg.get('active_model')}'.",
        "active_model": cfg.get("active_model"),
        "gemini_configured": bool(cfg.get("gemini_api_key")),
    }


@router.post("/verify-gemini-token")
async def verify_gemini_token(req: VerifyTokenRequest):
    key = req.gemini_api_key.strip()
    if not key:
        raise HTTPException(status_code=400, detail="Gemini API Key cannot be empty.")

    try:
        import google.generativeai as genai
        genai.configure(api_key=key)

        # Quick test generation with minimal tokens
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content("Say 'OK'")
        if resp and resp.text:
            return {
                "valid": True,
                "message": "Token successfully verified! Connected to Google Gemini 1.5 Flash.",
                "model": "gemini-1.5-flash",
                "free_tier_limits": "15 Requests/Min, 1,500 Requests/Day Free"
            }
        else:
            raise Exception("No response received from Google Gemini API.")
    except Exception as e:
        err_msg = str(e)
        if "API_KEY_INVALID" in err_msg or "400" in err_msg:
            err_msg = "Invalid API Key. Please verify you copied the full key starting with 'AIzaSy' from Google AI Studio."
        elif "ResourceExhausted" in err_msg or "429" in err_msg:
            err_msg = "Quota exceeded on this key. Please check your Google AI Studio quota."
        return {
            "valid": False,
            "error": err_msg
        }
