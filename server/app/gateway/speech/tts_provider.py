from abc import ABC, abstractmethod
from typing import Optional


class TTSProvider(ABC):
    """
    Abstract base class for TTS providers.
    Defines the interface that all TTS implementations must follow.
    """

    @abstractmethod
    def synthesize(
        self, text: str, language: str = "Japanese", **kwargs
    ) -> Optional[bytes]:
        """
        Synthesize text to speech audio bytes.

        :param text: Text to synthesize.
        :param language: Language code (e.g., "Japanese").
        :return: Audio bytes or None if failed.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the TTS provider is available and responding.

        :return: True if available, False otherwise.
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get the name of the provider.

        :return: Provider name (e.g., "mlx-tts", "openrouter-tts").
        """
        pass


class MLXTTSProvider(TTSProvider):
    """
    MLX-local TTS provider using Qwen3-TTS models.
    Follows the pattern from /Users/kaleb/Documents/Code/tts/run_tts.py
    """

    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip("/")

    def synthesize(
        self, text: str, language: str = "Japanese", **kwargs
    ) -> Optional[bytes]:
        import requests

        try:
            response = requests.post(
                f"{self.server_url}/v1/audio/speech",
                json={
                    "input": text,
                    "model": kwargs.get(
                        "model", "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit"
                    ),
                    "voice": kwargs.get("voice", "default"),
                    "language": language,
                },
                timeout=60,
            )
            response.raise_for_status()
            return response.content
        except Exception:
            return None

    def is_available(self) -> bool:
        import requests

        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def get_provider_name(self) -> str:
        return "mlx-tts"


class OpenRouterTTSProvider(TTSProvider):
    """
    OpenRouter TTS provider (e.g., Qwen TTS / Bark via OpenRouter API).
    """

    def __init__(
        self, api_key: str, model: str, base_url: str = "https://openrouter.ai/api/v1"
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")

    def synthesize(
        self, text: str, language: str = "Japanese", **kwargs
    ) -> Optional[bytes]:
        import requests

        try:
            response = requests.post(
                f"{self.base_url}/v1/audio/speech",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "input": text,
                    "model": self.model,
                    "voice": kwargs.get("voice", "default"),
                },
                timeout=60,
            )
            response.raise_for_status()
            return response.content
        except Exception:
            return None

    def is_available(self) -> bool:
        import requests

        try:
            response = requests.get(f"{self.base_url}/models", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def get_provider_name(self) -> str:
        return f"openrouter-tts-{self.model}"
