from app.gateway.speech import transcribe as stt_gateway_transcribe
from app.module.logging_module import logger


def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcribe audio bytes to text using the configured STT provider.

    :param audio_bytes: Raw audio data.
    :return: Transcribed text.
    :raises Exception: If the provider returns no response.
    """
    logger.debug("STT Service: Transcribing audio...")
    result = stt_gateway_transcribe(audio_bytes)
    if result is None:
        logger.error("STT Service: Provider returned no transcription.")
        raise Exception("STT provider returned no response. Check logs.")
    logger.debug(f"STT Service: Transcription result: {result[:50]}...")
    return result


def get_stt_status() -> dict:
    """
    Get the status of the STT provider.

    :return: Dictionary with STT provider status.
    """
    from app.gateway.speech import get_provider_info

    info = get_provider_info()
    return {"stt": info["stt"]}
