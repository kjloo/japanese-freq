import requests

from app.module.logging_module import logger
from app.gateway.llm.llm_provider import LLMProvider


class OpenRouterProvider(LLMProvider):
    """
    LLM provider for OpenRouter.
    Uses the OpenRouter API for LLM inference.
    """

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float = 0.7,
        timeout: int = 120,
        base_url: str = "https://openrouter.ai/api/v1",
    ):
        """
        Initialize the OpenRouter provider.

        :param api_key: OpenRouter API key.
        :param model: Model identifier (e.g., "openai/gpt-4-turbo").
        :param temperature: Sampling temperature.
        :param timeout: Request timeout in seconds.
        :param base_url: Base URL for OpenRouter API.
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.base_url = base_url

    def generate(self, prompt: str, system_prompt: str, max_tokens: int) -> str | None:
        """
        Send a request to OpenRouter API and get the response.

        :param prompt: The user's prompt.
        :param system_prompt: The system prompt.
        :param max_tokens: Maximum tokens to generate.
        :return: Generated text or None if failed.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "temperature": self.temperature,
                "max_tokens": max_tokens,
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()

            # Parse the OpenAI-compatible response structure
            if "choices" in data and len(data["choices"]) > 0:
                choice = data["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    return choice["message"]["content"]
                elif "text" in choice:
                    return choice["text"]

            logger.error(f"❌ OpenRouter returned unexpected structure: {data}")
            return None

        except requests.exceptions.HTTPError as e:
            logger.error(
                f"❌ OpenRouter HTTP Error: {e.response.status_code} - {e.response.text}"
            )
            return None
        except Exception as e:
            logger.error(f"❌ OpenRouter Error: {type(e).__name__} - {e}")
            return None

    def is_loaded(self) -> bool:
        """
        Check if OpenRouter API is accessible.

        :return: True if the API is accessible, False otherwise.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }
            response = requests.get(
                f"{self.base_url}/models", headers=headers, timeout=2
            )
            return response.status_code == 200
        except Exception:
            return False

    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "openrouter"
