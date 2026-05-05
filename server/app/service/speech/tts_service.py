from app.gateway.speech import synthesize as tts_gateway_synthesize
from app.module.logging_module import logger


def synthesize_speech(text: str, language: str = "Japanese", **kwargs) -> bytes:
    """
    Synthesize text to speech audio using the configured TTS provider.

    :param text: Text to synthesize.
    :param language: Language for synthesis.
    :return: Audio bytes.
    :raises Exception: If the provider returns no response.
    """
    logger.debug(f"TTS Service: Synthesizing text: {text[:50]}...")
    result = tts_gateway_synthesize(text, language=language, **kwargs)
    if result is None:
        logger.error("TTS Service: Provider returned no audio.")
        raise Exception("TTS provider returned no response. Check logs.")
    logger.debug("TTS Service: Synthesis successful.")
    return result


def get_tts_status() -> dict:
    """
    Get the status of the TTS provider.

    :return: Dictionary with TTS provider status.
    """
    from app.gateway.speech import get_provider_info

    info = get_provider_info()
    return {"tts": info["tts"]}
