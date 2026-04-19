import pytest
from unittest.mock import patch, MagicMock
from app.service.llm import llm_service


@patch("app.module.llm_module.llm_module.get_model_and_tokenizer")
@patch("app.service.llm.llm_service.generate")
def test_prompt_llm_calls_generate(mock_generate, mock_get_assets):
    # Setup mocks
    mock_model = MagicMock()
    mock_tokenizer = MagicMock()
    mock_get_assets.return_value = (mock_model, mock_tokenizer)

    # Mock the tokenizer's chat template application
    mock_tokenizer.apply_chat_template.return_value = "<formatted_prompt>"
    mock_generate.return_value = "こんにちは！"

    # Execute
    response = llm_service.prompt_llm(
        user_prompt="Hello", system_prompt="You are helpful", max_tokens=100
    )

    # Assertions
    assert response == "こんにちは！"
    mock_tokenizer.apply_chat_template.assert_called_once()
    mock_generate.assert_called_once_with(
        mock_model,
        mock_tokenizer,
        prompt="<formatted_prompt>",
        max_tokens=100,
        temp=0.7,
    )


def test_get_llm_status():
    status = llm_service.get_llm_status()
    assert "loaded" in status
    assert "model_path" in status
