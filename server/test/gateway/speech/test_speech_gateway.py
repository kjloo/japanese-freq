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
    mock_provider = mock.Mock()
    mock_provider.transcribe.return_value = "result_text"
    mocker.patch("app.gateway.speech.stt_provider.stt_provider", mock_provider)

    out = transcribe(FAKE_AUDIO)
    assert out == "result_text"
    mock_provider.transcribe.assert_called_once_with(FAKE_AUDIO)


def test_transcribe_raises_on_none(mocker):
    mock_provider = mock.Mock()
    mock_provider.transcribe.return_value = None
    mocker.patch("app.gateway.speech.stt_provider.stt_provider", mock_provider)

    with pytest.raises(Exception) as exc:
        transcribe(FAKE_AUDIO)
    assert "no transcription" in str(exc.value).lower()


def test_synthesize_delegates(mocker):
    mock_provider = mock.Mock()
    mock_provider.synthesize.return_value = b"audio_bytes"
    mocker.patch("app.gateway.speech.tts_provider.tts_provider", mock_provider)

    out = synthesize(FAKE_TEXT)
    assert out == b"audio_bytes"
    mock_provider.synthesize.assert_called_once_with(FAKE_TEXT, language="Japanese")


def test_synthesize_raises_on_none(mocker):
    mock_provider = mock.Mock()
    mock_provider.synthesize.return_value = None
    mocker.patch("app.gateway.speech.tts_provider.tts_provider", mock_provider)

    with pytest.raises(Exception) as exc:
        synthesize(FAKE_TEXT)
    assert "no audio" in str(exc.value).lower()


def test_get_provider_info(mocker):
    mock_stt = mock.Mock()
    mock_stt.get_provider_name.return_value = "stt-mock"
    mock_stt.is_available.return_value = True
    mock_tts = mock.Mock()
    mock_tts.get_provider_name.return_value = "tts-mock"
    mock_tts.is_available.return_value = False

    mocker.patch("app.gateway.speech.stt_provider.stt_provider", mock_stt)
    mocker.patch("app.gateway.speech.tts_provider.tts_provider", mock_tts)

    info = get_provider_info()
    assert info["stt"]["provider"] == "stt-mock"
    assert info["tts"]["provider"] == "tts-mock"
    assert info["stt"]["available"] is True
    assert info["tts"]["available"] is False


def test_is_stt_available(mocker):
    mock_stt = mock.Mock(is_available=mock.Mock(return_value=True))
    with mock.patch(
        "app.gateway.speech.stt_provider.stt_provider", return_value=mock_stt
    ):
        assert is_stt_available() is True


def test_is_tts_available(mocker):
    mock_tts = mock.Mock(is_available=mock.Mock(return_value=False))
    with mock.patch(
        "app.gateway.speech.tts_provider.tts_provider", return_value=mock_tts
    ):
        assert is_tts_available() is False
