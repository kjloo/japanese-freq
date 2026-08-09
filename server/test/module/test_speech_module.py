import pytest
from unittest import mock
from app.module import speech_module


def test_speech_module_import_does_not_crash():
    """Importing the module should not raise."""
    assert speech_module is not None


def test_speech_module_has_providers():
    """Module should have stt_provider and tts_provider attributes."""
    assert hasattr(speech_module, "stt_provider")
    assert hasattr(speech_module, "tts_provider")


def test_create_stt_provider_mlx(mocker):
    """Factory should create MLXSTTProvider when config selects MLX."""
    mock_config = mocker.Mock()
    mock_config.stt_provider = "mlx"
    mock_config.mlx_stt_server_url = "http://mlx-stt.local"

    mock_mlx_provider = mocker.patch("app.module.speech_module.MLXSTTProvider")
    # Set the speech_config in the module to our mock
    mocker.patch.object(speech_module, "speech_config", mock_config)

    provider = speech_module._create_stt_provider()
    mock_mlx_provider.assert_called_once_with(server_url="http://mlx-stt.local")
    assert provider == mock_mlx_provider.return_value


def test_create_stt_provider_openrouter(mocker):
    """Factory should create OpenRouterSTTProvider when config selects OpenRouter."""
    mock_config = mocker.Mock()
    mock_config.stt_provider = "openrouter"
    mock_config.openrouter_stt_model = "openai/whisper-large-v3"
    mock_config.openrouter_api_key = "fake-key"
    mock_config.openrouter_base_url = "https://openrouter.ai/api/v1"

    mock_or_provider = mocker.patch("app.module.speech_module.OpenRouterSTTProvider")
    mocker.patch.object(speech_module, "speech_config", mock_config)

    provider = speech_module._create_stt_provider()
    mock_or_provider.assert_called_once_with(
        api_key="fake-key",
        model="openai/whisper-large-v3",
        base_url="https://openrouter.ai/api/v1",
    )
    assert provider == mock_or_provider.return_value


def test_create_tts_provider_mlx(mocker):
    mock_config = mocker.Mock()
    mock_config.tts_provider = "mlx"
    mock_config.mlx_tts_server_url = "http://mlx-tts.local"

    mock_mlx_provider = mocker.patch("app.module.speech_module.MLXTTSProvider")
    mocker.patch.object(speech_module, "speech_config", mock_config)

    provider = speech_module._create_tts_provider()
    mock_mlx_provider.assert_called_once_with(server_url="http://mlx-tts.local")
    assert provider == mock_mlx_provider.return_value


def test_create_tts_provider_openrouter(mocker):
    mock_config = mocker.Mock()
    mock_config.tts_provider = "openrouter"
    mock_config.openrouter_tts_model = "openai/tts-1"
    mock_config.openrouter_api_key = "fake-key"
    mock_config.openrouter_base_url = "https://openrouter.ai/api/v1"

    mock_or_provider = mocker.patch("app.module.speech_module.OpenRouterTTSProvider")
    mocker.patch.object(speech_module, "speech_config", mock_config)

    provider = speech_module._create_tts_provider()
    mock_or_provider.assert_called_once_with(
        api_key="fake-key",
        model="openai/tts-1",
        base_url="https://openrouter.ai/api/v1",
    )
    assert provider == mock_or_provider.return_value


def test_speech_module_instantiates_providers(mocker):
    """Ensure that the module-level stt_provider and tts_provider are set."""
    # This test just verifies that the module loaded without error.
    # The actual values depend on the environment (env variable SPEECH_CONFIG).
    assert speech_module.stt_provider is not None
    assert speech_module.tts_provider is not None
