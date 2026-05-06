import pytest
from unittest import mock
from app.gateway.speech.tts_provider import (
    TTSProvider,
    MLXTTSProvider,
    OpenRouterTTSProvider,
)


def test_tts_provider_cannot_instantiate():
    """TTSProvider cannot be instantiated without implementing abstract methods."""
    with pytest.raises(TypeError):
        TTSProvider()


def test_mlx_tts_constructor():
    p = MLXTTSProvider(server_url="http://localhost:8082/v1")
    assert p.server_url == "http://localhost:8082/v1"


def test_mlx_tts_synthesize_success(mocker):
    fake_resp = mock.Mock()
    fake_resp.content = b"fake mp3"
    fake_resp.raise_for_status.return_value = None
    mocker.patch("requests.post", return_value=fake_resp)

    provider = MLXTTSProvider(server_url="http://localhost:8082/v1")
    out = provider.synthesize("こんにちは", language="Japanese")
    assert out == b"fake mp3"


def test_mlx_tts_synthesize_failure(mocker):
    mocker.patch("requests.post", side_effect=Exception("network"))
    provider = MLXTTSProvider(server_url="http://localhost:8082/v1")
    out = provider.synthesize("こんにちは", language="Japanese")
    assert out is None


def test_openrouter_tts_constructor():
    p = OpenRouterTTSProvider(
        api_key="key", model="openai/gpt-tts", base_url="https://openrouter.ai/api/v1"
    )
    assert p.api_key == "key"
    assert p.model == "openai/gpt-tts"


def test_openrouter_tts_synthesize_success(mocker):
    fake_resp = mock.Mock()
    fake_resp.content = b"fake mp3"
    fake_resp.raise_for_status.return_value = None
    mocker.patch("requests.post", return_value=fake_resp)

    provider = OpenRouterTTSProvider(
        api_key="key", model="openai/gpt-tts", base_url="https://openrouter.ai/api/v1"
    )
    out = provider.synthesize("テスト", language="Japanese")
    assert out == b"fake mp3"


def test_is_available(mocker):
    mocker.patch("requests.get", return_value=mock.Mock(status_code=200))
    provider = MLXTTSProvider(server_url="http://localhost:8082/v1")
    assert provider.is_available() is True
