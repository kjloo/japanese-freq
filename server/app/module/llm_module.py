import os
import requests
from app.module.logging_module import logger

# Get URL from Env, default to localhost for local dev
LLM_SERVER_URL = os.getenv("LLM_SERVER_URL", "http://localhost:8080/v1")


class LLMModule:
    def __init__(self):
        self.base_url = LLM_SERVER_URL
        self.model_name = "mlx-community/Qwen3.5-9B-MLX-4bit"

    def generate(self, prompt: str, system_prompt: str, max_tokens: int) -> str | None:
        """Sends a request to the sidecar MLX server."""
        try:
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.7,
                "max_tokens": max_tokens,
                "stream": False,  # Explicitly tell the server not to stream
            }

            response = requests.post(
                f"{self.base_url}/chat/completions", json=payload, timeout=120
            )
            response.raise_for_status()

            data = response.json()

            # Robust parsing of the OpenAI-compatible response structure
            if "choices" in data and len(data["choices"]) > 0:
                choice = data["choices"][0]
                # Some servers put the text in 'text', others in 'message' -> 'content'
                if "message" in choice and "content" in choice["message"]:
                    return choice["message"]["content"]
                elif "text" in choice:
                    return choice["text"]

            logger.error(f"❌ LLM Sidecar returned unexpected structure: {data}")
            return None

        except Exception as e:
            # This captures the 'content' KeyError as well as connection issues
            logger.error(f"❌ LLM Sidecar Error: {type(e).__name__} - {e}")
            return None

    @property
    def is_loaded(self) -> bool:
        try:
            return requests.get(f"{self.base_url}/models", timeout=2).status_code == 200
        except Exception:
            return False


llm_module = LLMModule()
