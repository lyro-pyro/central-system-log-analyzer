"""
Security module — provides API Key validation and IP-based rate limiting.
Ensures the backend cannot be abused.
"""

import time
from collections import defaultdict
from fastapi import Request, Security, HTTPException
from fastapi.security import APIKeyHeader
from app.core.config import settings

API_KEY_NAME = "X-API-KEY"
API_KEY_VALUE = "heimdall-secret-key"  # Hardcoded for hackathon, moved to ENV for prod
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Simple memory storage for rate limiting (ip -> list[timestamps])
rate_limit_table = defaultdict(list)
MAX_REQUESTS = 30
WINDOW_SEC = 60

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verifies that the X-API-KEY header matches our secret."""
    if not api_key or api_key != API_KEY_VALUE:
        raise HTTPException(
            status_code=401, 
            detail="Forbidden: Invalid or missing X-API-KEY header"
        )
    return api_key

async def check_rate_limit(request: Request):
    """Memory-based Rate Limiter by IP Address."""
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    
    # Evict timestamps older than our window
    rate_limit_table[client_ip] = [t for t in rate_limit_table[client_ip] if now - t < WINDOW_SEC]
    
    if len(rate_limit_table[client_ip]) >= MAX_REQUESTS:
        raise HTTPException(
            status_code=429, 
            detail="Too Many Requests. Rate limit exceeded."
        )
        
    rate_limit_table[client_ip].append(now)
    return client_ip
