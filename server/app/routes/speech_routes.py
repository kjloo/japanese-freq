from flask import Blueprint, jsonify, Response, request
from app.service.speech import stt_service, tts_service
from app.module.logging_module import logger

speech_routes = Blueprint("speech_routes", __name__)


@speech_routes.route("/api/speech/stt", methods=["POST"])
def stt() -> Response:
    """
    Speech-to-Text endpoint.
    Expects a file upload with key 'audio'.
    Returns JSON with transcribed text.
    """
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    audio_bytes = audio_file.read()

    try:
        text = stt_service.transcribe_audio(audio_bytes)
        return jsonify({"text": text}), 200
    except Exception as e:
        logger.error(f"speech_routes.py.stt: STT failed: {str(e)}")
        return jsonify({"error": "Internal STT error"}), 500


@speech_routes.route("/api/speech/tts", methods=["POST"])
def tts() -> Response:
    """
    Text-to-Speech endpoint.
    Expects JSON with 'text' field.
    Returns audio bytes.
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"]
    language = data.get("language", "Japanese")

    try:
        audio_bytes = tts_service.synthesize_speech(text, language=language)
        return Response(audio_bytes, mimetype="audio/mp3")
    except Exception as e:
        logger.error(f"speech_routes.py.tts: TTS failed: {str(e)}")
        return jsonify({"error": "Internal TTS error"}), 500


@speech_routes.route("/api/speech/status", methods=["GET"])
def status() -> Response:
    """
    Get status of STT and TTS providers.
    """
    from app.gateway.speech import get_provider_info

    return jsonify(get_provider_info()), 200
