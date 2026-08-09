import os
import sys
from pathlib import Path
from unittest import mock

import pytest
from flask import Flask

# Mock external modules that may not be installed
sys.modules["mlx_audio"] = mock.MagicMock()
sys.modules["mlx_audio.tts"] = mock.MagicMock()
sys.modules["mlx_audio.tts.utils"] = mock.MagicMock()
sys.modules["soundfile"] = mock.MagicMock()

# Ensure the server directory is on sys.path before importing the sidecar
SERVER_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SERVER_DIR))

# ruff: noqa: E402
from tts_sidecar import app as sidecar_app


@pytest.fixture
def client():
    sidecar_app.config["TESTING"] = True
    with sidecar_app.test_client() as client:
        yield client


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("status") == "ok"


def test_clone_missing_voice(client):
    resp = client.post(
        "/v1/audio/speech",
        json={"input": "test", "mode": "clone"},
    )
    assert resp.status_code == 400
    assert b"Missing 'voice'" in resp.data


def test_clone_invalid_voice_format(client):
    resp = client.post(
        "/v1/audio/speech",
        json={"input": "test", "mode": "clone", "voice": "badformat"},
    )
    assert resp.status_code == 400
    assert b"Voice must be in 'name|label' format" in resp.data


def test_clone_success(client, mocker):
    # Patch the load_reference_from_jsonl where it is used in tts_sidecar
    mocker.patch(
        "tts_sidecar.load_reference_from_jsonl",
        return_value={"audio": "wavs/kaleb_normal.wav", "text": "hello"},
    )
    # Mock Path.is_file to return True (reference audio exists)
    mocker.patch("pathlib.Path.is_file", return_value=True)
    # Mock the model and its generate method
    mock_model = mock.MagicMock()
    mock_result = mock.MagicMock()
    # Simulate numpy array .tobytes() method
    mock_result.audio = mock.MagicMock()
    mock_result.audio.tobytes.return_value = b"fake_wav_bytes"
    mock_model.generate.return_value = [mock_result]
    mock_model.sample_rate = 24000
    mocker.patch("tts_sidecar.load_model", return_value=mock_model)

    resp = client.post(
        "/v1/audio/speech",
        json={
            "input": "こんにちは",
            "mode": "clone",
            "voice": "kaleb|normal",
        },
    )
    assert resp.status_code == 200
    assert resp.mimetype == "audio/wav"
    assert resp.data == b"fake_wav_bytes"
