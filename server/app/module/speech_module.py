from app.module.logging_module import logger
from app.module.config.speech_config import SpeechConfig
from app.gateway.speech.stt_provider import MLXSTTProvider, OpenRouterSTTProvider
from app.gateway.speech.tts_provider import MLXTTSProvider, OpenRouterTTSProvider

speech_config = SpeechConfig()


def _create_stt_provider():
    """
    Factory function to create the appropriate STT provider.

    :return: An instance of the configured STT provider.
    """
    if speech_config.stt_provider == "mlx":
        logger.info(
            f"Initializing MLX STT provider with server: {speech_config.mlx_stt_server_url}"
        )
        return MLXSTTProvider(
            server_url=speech_config.mlx_stt_server_url,
        )
    elif speech_config.stt_provider == "openrouter":
        logger.info(
            f"Initializing OpenRouter STT provider with model: {speech_config.openrouter_stt_model}"
        )
        return OpenRouterSTTProvider(
            api_key=speech_config.openrouter_api_key,
            model=speech_config.openrouter_stt_model,
            base_url=speech_config.openrouter_base_url,
        )
    else:
        raise ValueError(f"Unknown STT provider: {speech_config.stt_provider}")


def _create_tts_provider():
    """
    Factory function to create the appropriate TTS provider.

    :return: An instance of the configured TTS provider.
    """
    if speech_config.tts_provider == "mlx":
        logger.info(
            f"Initializing MLX TTS provider with server: {speech_config.mlx_tts_server_url}"
        )
        return MLXTTSProvider(
            server_url=speech_config.mlx_tts_server_url,
        )
    elif speech_config.tts_provider == "openrouter":
        logger.info(
            f"Initializing OpenRouter TTS provider with model: {speech_config.openrouter_tts_model}"
        )
        return OpenRouterTTSProvider(
            api_key=speech_config.openrouter_api_key,
            model=speech_config.openrouter_tts_model,
            base_url=speech_config.openrouter_base_url,
        )
    else:
        raise ValueError(f"Unknown TTS provider: {speech_config.tts_provider}")


stt_provider = _create_stt_provider()
tts_provider = _create_tts_provider()

logger.info(
    f"✅ Speech Gateway initialized with STT: {stt_provider.get_provider_name()}, "
    f"TTS: {tts_provider.get_provider_name()}"
)
