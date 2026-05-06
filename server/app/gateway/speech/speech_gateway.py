from app.module.logging_module import logger
from app.module import speech_module


def transcribe(audio_bytes: bytes) -> str | None:
    """
    Transcribe audio using the configured STT provider.

    :param audio_bytes: Raw audio data.
    :return: Transcribed text or None if failed.
    """
    logger.debug("Speech Gateway: Transcribing audio...")
    result = speech_module.stt_provider.transcribe(audio_bytes)
    if result:
        logger.debug(f"Speech Gateway: Transcription: {result[:50]}...")
    else:
        logger.warning("Speech Gateway: STT provider returned no transcription.")
    return result


def synthesize(text: str, language: str = "Japanese", **kwargs) -> bytes | None:
    """
    Synthesize text to speech using the configured TTS provider.

    :param text: Text to synthesize.
    :param language: Language for synthesis.
    :return: Audio bytes or None if failed.
    """
    logger.debug(f"Speech Gateway: Synthesizing text: {text[:50]}...")
    result = speech_module.tts_provider.synthesize(text, language=language, **kwargs)
    if result:
        logger.debug("Speech Gateway: Synthesis successful.")
    else:
        logger.warning("Speech Gateway: TTS provider returned no audio.")
    return result


def is_stt_available() -> bool:
    return speech_module.stt_provider.is_available()


def is_tts_available() -> bool:
    return speech_module.tts_provider.is_available()


def get_provider_info() -> dict:
    """
    Get information about the configured STT and TTS providers.

    :return: Dictionary with provider information.
    """
    return {
        "stt": {
            "provider": speech_module.stt_provider.get_provider_name(),
            "available": is_stt_available(),
        },
        "tts": {
            "provider": speech_module.tts_provider.get_provider_name(),
            "available": is_tts_available(),
        },
    }
