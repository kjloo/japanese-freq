from abc import ABC, abstractmethod
from typing import Optional


class STTProvider(ABC):
    """
    Abstract base class for STT providers.
    Defines the interface that all STT implementations must follow.
    """

    @abstractmethod
    def transcribe(self, audio_bytes: bytes) -> Optional[str]:
        """
        Transcribe audio bytes to text.

        :param audio_bytes: Raw audio data.
        :return: Transcribed text or None if failed.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the STT provider is available and responding.

        :return: True if available, False otherwise.
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get the name of the provider.

        :return: Provider name (e.g., "mlx-stt", "openrouter-whisper").
        """
        pass


class MLXSTTProvider(STTProvider):
    """
    MLX-local STT provider.
    Calls a local MLX server endpoint for speech-to-text.
    """

    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip("/")

    def transcribe(self, audio_bytes: bytes) -> Optional[str]:
        import requests

        try:
            response = requests.post(
                f"{self.server_url}/audio/transcriptions",
                files={"file": ("audio.wav", audio_bytes, "audio/wav")},
                data={"model": "whisper"},
                timeout=30,
            )
            response.raise_for_status()
            return response.json().get("text")
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
        return "mlx-stt"


class OpenRouterSTTProvider(STTProvider):
    """
    OpenRouter STT provider (e.g., Whisper via OpenRouter API).
    """

    def __init__(
        self, api_key: str, model: str, base_url: str = "https://openrouter.ai/api/v1"
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")

    def transcribe(self, audio_bytes: bytes) -> Optional[str]:
        import requests

        try:
            response = requests.post(
                f"{self.base_url}/audio/transcriptions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                files={"file": ("audio.wav", audio_bytes, "audio/wav")},
                data={"model": self.model},
                timeout=30,
            )
            response.raise_for_status()
            return response.json().get("text")
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
        return f"openrouter-stt-{self.model}"
