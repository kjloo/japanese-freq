import pytest
from unittest import mock
from app.gateway.speech.stt_provider import (
    STTProvider,
    MLXSTTProvider,
    OpenRouterSTTProvider,
)

FAKE_AUDIO_BYTES = b"fake wav data"


def test_stt_provider_cannot_instantiate():
    """STTProvider cannot be instantiated without implementing abstract methods."""
    with pytest.raises(TypeError):
        STTProvider()


def test_mlx_stt_constructor():
    p = MLXSTTProvider(server_url="http://localhost:8081/v1")
    assert p.server_url == "http://localhost:8081/v1"


def test_mlx_stt_transcribe_success(mocker):
    fake_resp = mock.Mock()
    fake_resp.json.return_value = {"text": "こんにちは"}
    mocker.patch("requests.post", return_value=fake_resp)

    provider = MLXSTTProvider(server_url="http://localhost:8081/v1")
    out = provider.transcribe(b"dummy_audio")
    assert out == "こんにちは"


def test_mlx_stt_transcribe_failure(mocker):
    mocker.patch("requests.post", side_effect=Exception("network"))
    provider = MLXSTTProvider(server_url="http://localhost:8081/v1")
    out = provider.transcribe(b"audio")
    assert out is None


def test_openrouter_stt_constructor():
    p = OpenRouterSTTProvider(
        api_key="key",
        model="openai/whisper-large-v3",
        base_url="https://openrouter.ai/api/v1",
    )
    assert p.api_key == "key"
    assert p.model == "openai/whisper-large-v3"


def test_openrouter_stt_transcribe_success(mocker):
    fake_resp = mock.Mock()
    fake_resp.json.return_value = {"text": "テスト"}
    fake_resp.raise_for_status.return_value = None
    mocker.patch("requests.post", return_value=fake_resp)

    provider = OpenRouterSTTProvider(
        api_key="key",
        model="openai/whisper-large-v3",
        base_url="https://openrouter.ai/api/v1",
    )
    out = provider.transcribe(b"dummy_audio")
    assert out == "テスト"


def test_is_available(mocker):
    mocker.patch("requests.get", return_value=mock.Mock(status_code=200))
    provider = MLXSTTProvider(server_url="http://localhost:8081/v1")
    assert provider.is_available() is True
