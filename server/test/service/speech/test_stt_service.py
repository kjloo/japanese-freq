import pytest
from unittest import mock
from app.service.speech.stt_service import transcribe_audio, get_stt_status

FAKE_AUDIO = b"dummy_audio"


def test_transcribe_audio_success(mocker):
    """transcribe_audio() should return mocked result."""
    mock_transcribe = mock.Mock(return_value="結果")
    mocker.patch("app.gateway.speech.transcribe", return_value=mock_transcribe)

    result = transcribe_audio(FAKE_AUDIO)
    assert result == "結果"
    mock_transcribe.assert_called_once_with(FAKE_AUDIO)


def test_transcribe_audio_raises_on_none(mocker):
    """transcribe_audio() should raise on failed response."""
    mocker.patch("app.gateway.speech.transcribe", return_value=None)

    with pytest.raises(Exception) as exc:
        transcribe_audio(FAKE_AUDIO)
    assert "no response" in str(exc.value).lower()


def test_get_stt_status_delegates(mocker):
    mock_info = {"stt": {"provider": "mock-stt", "available": True}}
    mocker.patch("app.gateway.speech.get_provider_info", return_value=mock_info)

    info = get_stt_status()
    assert info == {"stt": {"provider": "mock-stt", "available": True}}
    mock_info.assert_called_once()
