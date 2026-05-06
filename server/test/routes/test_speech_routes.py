import pytest
from unittest import mock
from flask import Flask
from app.routes.speech_routes import speech_routes

# Mocked audio bytes and text for tests
FAKE_AUDIO = b"fake audio data"
FAKE_TEXT = "こんにちは"


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(speech_routes)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_stt_endpoint_success(client, mocker):
    """POST /api/speech/stt returns transcribed text."""
    mock_transcribe = mock.Mock(return_value="こんにちは")
    mocker.patch("app.service.speech.transcribe_audio", return_value="こんにちは")

    # Simulate file upload
    data = {"audio": (FAKE_AUDIO, "test.wav")}
    response = client.post(
        "/api/speech/stt", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["text"] == "こんにちは"
    mock_transcribe.assert_called_once_with(FAKE_AUDIO)


def test_stt_endpoint_missing_file(client):
    """POST /api/speech/stt without audio file returns 400."""
    response = client.post("/api/speech/stt", data={})
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error"] == "No audio file provided"


def test_stt_endpoint_internal_error(client, mocker):
    """POST /api/speech/stt when service raises returns 500."""
    mocker.patch("app.service.speech.transcribe_audio", side_effect=Exception("boom"))
    data = {"audio": (FAKE_AUDIO, "test.wav")}
    response = client.post(
        "/api/speech/stt", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 500
    json_data = response.get_json()
    assert json_data["error"] == "Internal STT error"


def test_tts_endpoint_success(client, mocker):
    """POST /api/speech/tts returns audio."""
    mock_synthesize = mock.Mock(return_value=b"fake mp3 bytes")
    mocker.patch("app.service.speech.synthesize_speech", return_value=b"fake mp3 bytes")

    payload = {"text": "こんにちは", "language": "Japanese"}
    response = client.post("/api/speech/tts", json=payload)
    assert response.status_code == 200
    assert response.mimetype == "audio/mp3"
    assert response.data == b"fake mp3 bytes"
    mock_synthesize.assert_called_once_with("こんにちは", language="Japanese")


def test_tts_endpoint_missing_text(client):
    """POST /api/speech/tts without text returns 400."""
    response = client.post("/api/speech/tts", json={"language": "Japanese"})
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error"] == "No text provided"


def test_tts_endpoint_internal_error(client, mocker):
    """POST /api/speech/tts when service raises returns 500."""
    mocker.patch("app.service.speech.synthesize_speech", side_effect=Exception("boom"))
    payload = {"text": "こんにちは"}
    response = client.post("/api/speech/tts", json=payload)
    assert response.status_code == 500
    json_data = response.get_json()
    assert json_data["error"] == "Internal TTS error"


def test_status_endpoint(client, mocker):
    """GET /api/speech/status returns provider info."""
    mock_info = {
        "stt": {"provider": "test-stt", "available": True},
        "tts": {"provider": "test-tts", "available": False},
    }
    mocker.patch("app.gateway.speech.get_provider_info", return_value=mock_info)
    response = client.get("/api/speech/status")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data == mock_info
