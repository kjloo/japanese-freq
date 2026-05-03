import pytest
from unittest.mock import patch
from test.fixture.client_fixture import client


@pytest.mark.usefixtures("client")
# Patch the service where it is used in the routes
@patch("app.routes.llm_routes.llm_service.prompt_llm")
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
    # Updated to match current route output (no 'model' key)
    assert data["response"] == "Test response"
    assert len(data.keys()) == 1


@pytest.mark.usefixtures("client")
def test_generate_response_validation_error(client):
    # Send missing/empty prompt to trigger LLMPromptForm ValueError
    payload = {"prompt": ""}

    response = client.post("/api/llm/generate", json=payload)

    assert response.status_code == 400
    assert "error" in response.get_json()


@pytest.mark.usefixtures("client")
@patch("app.routes.llm_routes.llm_service.prompt_llm")
def test_generate_response_service_failure(mock_prompt, client):
    # Mock an unexpected crash in the service
    mock_prompt.side_effect = Exception("Sidecar unreachable")

    payload = {"prompt": "Hello", "system_prompt": "Helpful", "max_tokens": 100}

    response = client.post("/api/llm/generate", json=payload)

    assert response.status_code == 500
    assert response.get_json()["error"] == "Internal model error"


@pytest.mark.usefixtures("client")
@patch("app.routes.llm_routes.llm_service.get_llm_status")
def test_get_status_route(mock_status, client):
    mock_status.return_value = {"loaded": True, "model_path": "/models/mlx-test"}

    response = client.get("/api/llm/status")

    assert response.status_code == 200
    data = response.get_json()
    assert data["loaded"] is True
    assert data["model_path"] == "/models/mlx-test"
