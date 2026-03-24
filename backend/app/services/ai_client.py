"""
AI Client — async HTTP client for Hugging Face Inference API.
Provides graceful fallback if the AP is unavailable or fails.
"""

import httpx
import json

from app.core.config import settings
from app.core.logging_config import logger


class AIClient:
    """
    Async client for Hugging Face LLM inference.
    Used only for insight generation — detection is always deterministic.
    """

    def __init__(self):
        self.api_key = settings.HUGGINGFACE_API_KEY
        self.model = settings.HUGGINGFACE_MODEL
        self.timeout = settings.HUGGINGFACE_TIMEOUT
        self.base_url = f"https://api-inference.huggingface.co/models/{self.model}"

    async def generate(self, prompt: str) -> str | None:
        """
        Send a prompt to Hugging Face and return the generated text.
        Returns None if Hugging Face is unavailable.
        """
        if not self.api_key:
            logger.warning("Hugging Face API key not configured — using rule-based fallback")
            return None
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "temperature": 0.3,
                            "max_new_tokens": 256,
                            "return_full_text": False
                        },
                        "options": {
                            "wait_for_model": True
                        }
                    },
                )
                response.raise_for_status()
                data = response.json()
                
                # Hugging Face returns a list of dictionaries for text generation models
                if isinstance(data, list) and len(data) > 0:
                    result = data[0].get("generated_text", "").strip()
                else:
                    result = str(data)
                
                logger.info(f"Hugging Face response received ({len(result)} chars)")
                return result
        except httpx.ConnectError:
            logger.warning("Hugging Face API not reachable — using rule-based fallback")
            return None
        except httpx.TimeoutException:
            logger.warning("Hugging Face request timed out — using rule-based fallback")
            return None
        except Exception as e:
            logger.error(f"Hugging Face error: {e} — using rule-based fallback")
            return None

    async def is_available(self) -> bool:
        """Check if Hugging Face API key is set."""
        return bool(self.api_key)
