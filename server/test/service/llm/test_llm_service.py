import pytest
from unittest.mock import patch
from app.service.llm import llm_service


@patch("app.service.llm.llm_service.llm_gateway")
def test_prompt_llm_calls_gateway(mock_gateway):
    # Setup mock return value
    mock_gateway.generate.return_value = "こんにちは！"

    # Execute
    response = llm_service.prompt_llm(
        user_prompt="Hello", system_prompt="You are helpful", max_tokens=100
    )

    # Assertions
    assert response == "こんにちは！"
    mock_gateway.generate.assert_called_once_with(
        prompt="Hello", system_prompt="You are helpful", max_tokens=100
    )


@patch("app.service.llm.llm_service.llm_gateway")
def test_prompt_llm_raises_exception_on_none(mock_gateway):
    # Setup gateway to return None
    mock_gateway.generate.return_value = None

    # Execute and Assert
    with pytest.raises(Exception, match="LLM provider returned no response"):
        llm_service.prompt_llm("Hello", "System", 100)


@patch("app.service.llm.llm_service.llm_gateway")
def test_get_llm_status(mock_gateway):
    # Setup mock status data
    expected_status = {"loaded": True, "model_path": "/path/to/model"}
    mock_gateway.get_provider_info.return_value = expected_status

    status = llm_service.get_llm_status()

    assert status == expected_status
    mock_gateway.get_provider_info.assert_called_once()
