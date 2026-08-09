import pytest
from unittest import mock
from app.gateway.speech import (
    transcribe,
    synthesize,
    get_provider_info,
    is_stt_available,
    is_tts_available,
)

FAKE_AUDIO = b"fake_audio_bytes"
FAKE_TEXT = "テスト"


def test_transcribe_delegates(mocker):
    mock_stt = mock.Mock()
    mock_stt.transcribe.return_value = "result_text"
    mocker.patch("app.module.speech_module.stt_provider", mock_stt)

    result = transcribe(FAKE_AUDIO)
    assert result == "result_text"
    mock_stt.transcribe.assert_called_once_with(FAKE_AUDIO)


def test_transcribe_returns_none_on_failure(mocker):
    mock_stt = mock.Mock()
    mock_stt.transcribe.return_value = None
    mocker.patch("app.module.speech_module.stt_provider", mock_stt)

    result = transcribe(FAKE_AUDIO)
    assert result is None


def test_synthesize_delegates(mocker):
    mock_tts = mock.Mock()
    mock_tts.synthesize.return_value = b"audio_bytes"
    mocker.patch("app.module.speech_module.tts_provider", mock_tts)

    result = synthesize(FAKE_TEXT)
    assert result == b"audio_bytes"
    mock_tts.synthesize.assert_called_once_with(FAKE_TEXT, language="Japanese")


def test_synthesize_returns_none_on_failure(mocker):
    mock_tts = mock.Mock()
    mock_tts.synthesize.return_value = None
    mocker.patch("app.module.speech_module.tts_provider", mock_tts)

    result = synthesize(FAKE_TEXT)
    assert result is None


def test_get_provider_info(mocker):
    mock_stt = mock.Mock()
    mock_stt.get_provider_name.return_value = "stt-mock"
    mock_stt.is_available.return_value = True
    mock_tts = mock.Mock()
    mock_tts.get_provider_name.return_value = "tts-mock"
    mock_tts.is_available.return_value = False

    mocker.patch("app.module.speech_module.stt_provider", mock_stt)
    mocker.patch("app.module.speech_module.tts_provider", mock_tts)

    info = get_provider_info()
    assert info["stt"]["provider"] == "stt-mock"
    assert info["tts"]["provider"] == "tts-mock"
    assert info["stt"]["available"] is True
    assert info["tts"]["available"] is False


def test_is_stt_available(mocker):
    mock_stt = mock.Mock(is_available=mock.Mock(return_value=True))
    mocker.patch("app.module.speech_module.stt_provider", mock_stt)

    assert is_stt_available() is True
    mock_stt.is_available.assert_called_once()


def test_is_tts_available(mocker):
    mock_tts = mock.Mock(is_available=mock.Mock(return_value=False))
    mocker.patch("app.module.speech_module.tts_provider", mock_tts)

    assert is_tts_available() is False
    mock_tts.is_available.assert_called_once()
