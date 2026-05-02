import requests
from app.module.logging_module import logger
from app.module.llm_provider import LLMProvider


class MLXProvider(LLMProvider):
    """
    LLM provider for MLX (Sidecar MLX server).
    Communicates with a local MLX server via HTTP.
    """

    def __init__(
        self,
        server_url: str,
        model_name: str,
        temperature: float = 0.7,
        timeout: int = 120,
    ):
        """
        Initialize the MLX provider.

        :param server_url: Base URL of the MLX server (e.g., "http://localhost:8080/v1").
        :param model_name: Name of the model to use.
        :param temperature: Sampling temperature.
        :param timeout: Request timeout in seconds.
        """
        self.base_url = server_url
        self.model_name = model_name
        self.temperature = temperature
        self.timeout = timeout

    def generate(self, prompt: str, system_prompt: str, max_tokens: int) -> str | None:
        """
        Send a request to the MLX server and get the response.

        :param prompt: The user's prompt.
        :param system_prompt: The system prompt.
        :param max_tokens: Maximum tokens to generate.
        :return: Generated text or None if failed.
        """
        try:
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "temperature": self.temperature,
                "max_tokens": max_tokens,
                "stream": False,
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
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

            logger.error(f"❌ MLX Server returned unexpected structure: {data}")
            return None

        except Exception as e:
            logger.error(f"❌ MLX Server Error: {type(e).__name__} - {e}")
            return None

    def is_loaded(self) -> bool:
        """
        Check if the MLX server is available.

        :return: True if the server is responsive, False otherwise.
        """
        try:
            response = requests.get(f"{self.base_url}/models", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "mlx"
