import pytest
from unittest import mock
from app.service.speech.tts_service import synthesize_speech, get_tts_status

FAKE_TEXT = "テスト"


def test_synthesize_speech_success(mocker):
    """synthesize_speech() returns mocked audio."""
    mock_synthesize = mock.Mock(return_value=b"mock_audio")
    mocker.patch(
        "app.service.speech.tts_service.tts_gateway_synthesize", mock_synthesize
    )

    result = synthesize_speech(FAKE_TEXT)
    assert result == b"mock_audio"
    mock_synthesize.assert_called_once_with(FAKE_TEXT, language="Japanese")


def test_synthesize_speech_raises_on_none(mocker):
    mocker.patch(
        "app.service.speech.tts_service.tts_gateway_synthesize",
        mock.Mock(return_value=None),
    )

    with pytest.raises(Exception) as exc:
        synthesize_speech(FAKE_TEXT)
    assert "no audio" in str(exc.value).lower()


def test_get_tts_status_delegates(mocker):
    """get_tts_status() should return provider info dictionary."""
    mock_info = {"tts": {"provider": "mock-tts", "available": True}}
    mock_get_info = mocker.patch(
        "app.gateway.speech.get_provider_info", return_value=mock_info
    )

    info = get_tts_status()
    assert info == {"tts": {"provider": "mock-tts", "available": True}}
    mock_get_info.assert_called_once()
