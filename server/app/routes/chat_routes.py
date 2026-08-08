"""
Chat Routes for Japanese Partner Chat Feature

This module handles the full conversation flow:
1. Client sends audio/text
2. STT converts speech to text
3. ConversationAssistant generates response
4. LLM generates final response
5. TTS converts response to speech
6. Response returned to client

All endpoints are RESTful and follow the existing architecture patterns.
"""

from flask import Blueprint, jsonify, request
from app.service.speech import stt_service, tts_service
from app.service.llm import llm_service
from app.assistant.conversation_assistant import ConversationAssistant
from app.module.logging_module import logger

chat_routes = Blueprint("chat_routes", __name__)


@chat_routes.route("/api/chat/message", methods=["POST"])
def send_message():
    """
    Chat message endpoint - handles the complete pipeline:
    Audio/Text → STT → Assistant → LLM → TTS → Audio

    Request can be:
    - multipart/form-data with 'audio' file
    - JSON with 'text' field

    Returns: JSON with transcript, assistant response, LLM response, and TTS audio
    """
    data = request.get_json(silent=True) or {}

    # Handle file upload (audio) via multipart/form-data
    if "audio" in request.files:
        audio_file = request.files["audio"]
        audio_bytes = audio_file.read()
        try:
            input_text = stt_service.transcribe_audio(audio_bytes)
        except Exception as e:
            logger.error(f"chat_routes.send_message: STT failed: {str(e)}")
            return jsonify({"error": "STT processing failed"}), 500
    # Handle JSON body (text)
    elif data and "text" in data:
        input_text = data.get("text", "")
    else:
        return jsonify({"error": "No audio file or text provided"}), 400

    if not input_text.strip():
        return jsonify({"error": "No input provided"}), 400

    # Step 1: Run through Conversation Assistant
    assistant = ConversationAssistant()
    assistant_output = assistant.process(input_text)

    # Step 2: Send to LLM for generation
    try:
        llm_response = llm_service.prompt_llm(
            user_prompt=input_text,
            system_prompt="You are a Japanese language partner. Respond naturally in Japanese to the user's message.",
            max_tokens=300,
        )
    except Exception as e:
        logger.error(f"chat_routes.send_message: LLM failed: {str(e)}")
        # Fallback to assistant response if LLM fails
        llm_response = input_text

    # Step 3: Convert response to speech
    try:
        tts_audio = tts_service.synthesize_speech(llm_response, language="Japanese")
    except Exception as e:
        logger.error(f"chat_routes.send_message: TTS failed: {str(e)}")
        tts_audio = None

    # Step 4: Return full response
    return (
        jsonify(
            {
                "success": True,
                "transcript": input_text,
                "assistant": assistant_output,
                "response": llm_response,
                "audio": tts_audio,
                "audio_format": "audio/mp3" if tts_audio else None,
            }
        ),
        200,
    )


@chat_routes.route("/api/chat/audio", methods=["POST"])
def send_audio_message():
    """
    Audio-only chat endpoint for microphone input.
    Accepts raw audio WAV bytes, runs STT, processing, and returns TTS audio.
    """
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    audio_bytes = audio_file.read()

    # Step 1: STT
    try:
        input_text = stt_service.transcribe_audio(audio_bytes)
    except Exception as e:
        logger.error(f"chat_routes.send_audio_message: STT failed: {str(e)}")
        return jsonify({"error": "STT processing failed"}), 500

    # Step 2: Assistant
    assistant = ConversationAssistant()
    assistant.process(input_text)

    # Step 3: LLM
    try:
        llm_response = llm_service.prompt_llm(
            user_prompt=input_text,
            system_prompt="You are a Japanese language partner. Respond naturally in Japanese to the user's message.",
            max_tokens=300,
        )
    except Exception as e:
        logger.error(f"chat_routes.send_audio_message: LLM failed: {str(e)}")
        # Fallback to a simple response if both fallbacks fail
        llm_response = input_text

    # Step 4: TTS
    try:
        tts_audio = tts_service.synthesize_speech(llm_response, language="Japanese")
    except Exception as e:
        logger.error(f"chat_routes.send_audio_message: TTS failed: {str(e)}")
        return jsonify({"error": "TTS synthesis failed"}), 500

    return (
        jsonify(
            {
                "success": True,
                "transcript": input_text,
                "response": llm_response,
                "audio": tts_audio,
            }
        ),
        200,
    )


@chat_routes.route("/api/chat/status", methods=["GET"])
def chat_status():
    """
    Get chat endpoint status.
    Returns STT and TTS provider status.
    """
    from app.gateway.speech import get_provider_info

    return jsonify(get_provider_info()), 200
