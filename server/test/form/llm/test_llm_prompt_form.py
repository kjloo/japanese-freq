import pytest
from app.form.llm.llm_prompt_form import LLMPromptForm


def test_form_validation_valid():
    data = {"prompt": "Valid prompt"}
    form = LLMPromptForm(data)
    assert form.prompt == "Valid prompt"
    # Test default system prompt
    assert "日本語" in form.system_prompt


def test_form_validation_missing_prompt():
    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        LLMPromptForm({"prompt": ""})


def test_form_validation_invalid_tokens():
    with pytest.raises(ValueError, match="max_tokens must be a positive integer"):
        LLMPromptForm({"prompt": "test", "max_tokens": -1})
