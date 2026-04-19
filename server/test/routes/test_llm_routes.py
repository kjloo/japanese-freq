import pytest
from unittest.mock import patch


@patch("app.service.llm.llm_service.prompt_llm")
def test_generate_response_success(mock_prompt, client):
    # Mock service return
    mock_prompt.return_value = "Test response"

    payload = {
        "prompt": "Explain 'nomu'",
        "system_prompt": "Expert mode",
        "max_tokens": 500,
    }

    response = client.post("/api/llm/generate", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data["response"] == "Test response"
    assert "model" in data


def test_generate_response_validation_error(client):
    # Send empty prompt to trigger LLMPromptForm ValueError
    payload = {"prompt": ""}

    response = client.post("/api/llm/generate", json=payload)

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_get_status_route(client):
    response = client.get("/api/llm/status")
    assert response.status_code == 200
    assert "loaded" in response.get_json()
