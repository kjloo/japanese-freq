import os


class SpeechConfig:
    def __init__(self, config: dict):
        """
        Initialize SpeechConfig by loading from YAML config and environment variables.

        :param config: The configuration dictionary from YAML.
        """
        speech_config = config.get("speech", {})

        # STT Provider: "mlx" or "openrouter"
        self.stt_provider = os.getenv(
            "STT_PROVIDER", speech_config.get("stt_provider", "mlx")
        )

        # TTS Provider: "mlx" or "openrouter"
        self.tts_provider = os.getenv(
            "TTS_PROVIDER", speech_config.get("tts_provider", "mlx")
        )

        # MLX STT settings
        self.mlx_stt_server_url = os.getenv(
            "MLX_STT_SERVER_URL",
            speech_config.get("mlx_stt_server_url", "http://localhost:8081/v1"),
        )

        # MLX TTS settings
        self.mlx_tts_server_url = os.getenv(
            "MLX_TTS_SERVER_URL",
            speech_config.get("mlx_tts_server_url", "http://localhost:8082/v1"),
        )
        self.mlx_tts_model_clone = os.getenv(
            "MLX_TTS_MODEL_CLONE",
            speech_config.get(
                "mlx_tts_model_clone", "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit"
            ),
        )
        self.mlx_tts_model_design = os.getenv(
            "MLX_TTS_MODEL_DESIGN",
            speech_config.get(
                "mlx_tts_model_design",
                "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16",
            ),
        )

        # OpenRouter STT settings
        self.openrouter_api_key = os.getenv(
            "OPENROUTER_API_KEY", speech_config.get("openrouter_api_key")
        )
        self.openrouter_stt_model = os.getenv(
            "OPENROUTER_STT_MODEL",
            speech_config.get("openrouter_stt_model", "openai/whisper-large-v3"),
        )

        # OpenRouter TTS settings
        self.openrouter_tts_model = os.getenv(
            "OPENROUTER_TTS_MODEL",
            speech_config.get("openrouter_tts_model", "openai/tts-1"),
        )
        self.openrouter_base_url = speech_config.get(
            "openrouter_base_url", "https://openrouter.ai/api/v1"
        )

        # Shared audio settings
        self.audio_format = speech_config.get("audio_format", "mp3")
        self.sample_rate = int(speech_config.get("sample_rate", 16000))
        self.tts_language = speech_config.get("tts_language", "Japanese")

    def validate(self) -> bool:
        """
        Validate the speech configuration for the selected providers.

        :return: True if valid, False otherwise.
        """
        stt_ok = False
        tts_ok = False

        if self.stt_provider == "mlx":
            stt_ok = bool(self.mlx_stt_server_url)
        elif self.stt_provider == "openrouter":
            stt_ok = bool(self.openrouter_api_key)
        else:
            return False

        if self.tts_provider == "mlx":
            tts_ok = bool(self.mlx_tts_server_url)
        elif self.tts_provider == "openrouter":
            tts_ok = bool(self.openrouter_api_key)
        else:
            return False

        return stt_ok and tts_ok
