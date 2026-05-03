import pytest
from unittest.mock import patch, MagicMock
from app.gateway.llm import llm_gateway


@patch("app.gateway.llm.llm_gateway.llm_provider")
def test_generate_success(mock_provider):
    # Setup
    mock_provider.generate.return_value = "Success response"
    prompt = "Hello"
    system_prompt = "You are a helpful assistant"
    max_tokens = 100

    # Execute
    result = llm_gateway.generate(prompt, system_prompt, max_tokens)

    # Assert
    assert result == "Success response"
    mock_provider.generate.assert_called_once_with(prompt, system_prompt, max_tokens)


@patch("app.gateway.llm.llm_gateway.llm_provider")
def test_generate_failure(mock_provider):
    # Setup: Provider returns None on failure
    mock_provider.generate.return_value = None

    # Execute
    result = llm_gateway.generate("prompt", "system", 10)

    # Assert
    assert result is None
    mock_provider.generate.assert_called_once()


@patch("app.gateway.llm.llm_gateway.llm_provider")
def test_is_available(mock_provider):
    # Test True
    mock_provider.is_loaded.return_value = True
    assert llm_gateway.is_available() is True

    # Test False
    mock_provider.is_loaded.return_value = False
    assert llm_gateway.is_available() is False


@patch("app.gateway.llm.llm_gateway.llm_config")
@patch("app.gateway.llm.llm_gateway.llm_provider")
def test_get_provider_info(mock_provider, mock_config):
    # Setup mock data
    mock_provider.get_provider_name.return_value = "MLX_Provider"
    mock_provider.is_loaded.return_value = True

    mock_config.temperature = 0.7
    mock_config.max_tokens = 2048
    mock_config.timeout = 30

    # Execute
    info = llm_gateway.get_provider_info()

    # Assert
    assert info["provider"] == "MLX_Provider"
    assert info["available"] is True
    assert info["config"]["temperature"] == 0.7
    assert info["config"]["timeout"] == 30
