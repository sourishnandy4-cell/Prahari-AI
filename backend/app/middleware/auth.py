"""
API Key Authentication Middleware.

If API_KEY is set in settings/environment, all requests to /api/* must include:
  Header: X-API-Key: <your_key>

To enable: set API_KEY=your_secret_key in .env
To disable: leave API_KEY unset or empty in .env
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from backend.app.config import settings


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Only protect /api/* routes
        if request.url.path.startswith("/api/"):
            if settings.API_KEY:
                key = request.headers.get("X-API-Key", "")
                if key != settings.API_KEY:
                    return JSONResponse(
                        status_code=401,
                        content={
                            "error": "Unauthorized",
                            "detail": "Invalid or missing X-API-Key header. Set X-API-Key: <your_key> in request headers."
                        }
                    )
        return await call_next(request)
