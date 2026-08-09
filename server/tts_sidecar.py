"""Qwen 3 TTS sidecar server.

This server runs locally and provides a ``/v1/audio/speech`` endpoint compatible
with the existing ``MLXTTSProvider`` payload. It supports two modes:

* ``clone`` – voice cloning using a reference audio+text from the ``my_dataset``
  JSONL file. ``voice`` is expected as ``"<speaker_name>|<label>"`` (e.g.
  ``"kaleb|normal"``).
* ``design`` – instruction‑based synthesis (the original ``design`` mode from
  the standalone repo).

The implementation mirrors the logic in ``run_tts.py`` from the separate TTS
repository, re‑using the helper utilities in ``server/app/mapper/tts_utils.py``.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

from flask import Flask, jsonify, request

# Load utilities from the mapper package
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app.mapper.tts_utils import (
    load_reference_from_jsonl,
)

# MLX audio imports – optional for testing.
# If the package is unavailable, we provide a lightweight stub that raises
# a clear error only when the model is actually used.
try:
    from mlx_audio.tts.utils import load_model  # type: ignore
except Exception:  # pragma: no cover

    def load_model(*_args, **_kwargs):
        raise RuntimeError(
            "mlx_audio is required to run the TTS sidecar – install the 'mlx-audio' package to use this feature."
        )


app = Flask(__name__)

# ---------------------------------------------------------------------------
# Configuration – read from environment variables (fallback defaults match the
# original tts repo).
# ---------------------------------------------------------------------------
# Resolve dataset directory relative to this file for reliable path handling
BASE_DIR = Path(__file__).parent
DATASET_JSONL = os.getenv(
    "TTS_DATASET_JSONL",
    str(BASE_DIR / "app/mapper/tts_dataset/train.jsonl"),
)

# Model IDs – can be overridden via env vars for flexibility.
MODEL_CLONE = os.getenv(
    "MLX_TTS_MODEL_CLONE",
    "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit",
)
MODEL_DESIGN = os.getenv(
    "MLX_TTS_MODEL_DESIGN",
    "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16",
)

# Models will be loaded lazily on first request.
model_clone = None
model_design = None


def _parse_voice_string(voice: str) -> tuple[str, str]:
    """Parse ``voice`` expressed as ``"name|label"``.

    Returns a ``(name, label)`` tuple. Raises ``ValueError`` if the format is
    invalid.
    """
    if "|" not in voice:
        raise ValueError("Voice must be in 'name|label' format for clone mode")
    name, label = voice.split("|", 1)
    return name.strip(), label.strip()


@app.route("/v1/audio/speech", methods=["POST"])
def speech() -> Any:
    """Endpoint compatible with the existing MLX TTS provider.

    Expected JSON keys:
        - ``input`` (text to synthesize)
        - ``model`` (optional – ignored, the sidecar chooses based on mode)
        - ``voice`` (optional – required for ``clone`` mode, format ``name|label``)
        - ``language`` (default ``Japanese``)
        - ``mode`` (``clone`` or ``design`` – defaults to ``design``)
        - ``instruct`` (optional, used only in ``design`` mode)
    """
    payload: Dict[str, Any] = request.get_json(silent=True) or {}
    text = payload.get("input") or payload.get("text")
    if not text:
        return jsonify({"error": "Missing 'input'/'text' field"}), 400

    mode = payload.get("mode", "design")
    language = payload.get("language", "Japanese")

    # ---------------------------------------------------------------------
    # Clone mode – requires a reference audio and text from the dataset.
    # ---------------------------------------------------------------------
    if mode == "clone":
        voice = payload.get("voice")
        if not voice:
            return jsonify({"error": "Missing 'voice' for clone mode"}), 400
        try:
            name, label = _parse_voice_string(voice)
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400

        # Lazy load the clone model if not already loaded.
        global model_clone
        if model_clone is None:
            model_clone = load_model(MODEL_CLONE, fix_mistral_regex=True)
        # Load reference entry from the JSONL file.
        try:
            ref_entry = load_reference_from_jsonl(DATASET_JSONL, name, label)
        except Exception as exc:
            return jsonify({"error": f"Reference not found: {exc}"}), 400

        ref_audio_path = BASE_DIR / "app/mapper/tts_dataset" / ref_entry["audio"]
        if not ref_audio_path.is_file():
            return (
                jsonify({"error": f"Reference audio missing: {ref_audio_path}"}),
                500,
            )
        # The original repo passes ``ref_audio`` and ``ref_text`` to ``model.generate``.
        try:
            results = list(
                model_clone.generate(
                    text=text,
                    ref_audio=str(ref_audio_path),
                    ref_text=ref_entry.get("text", ""),
                    language=language,
                )
            )
        except Exception as exc:
            return jsonify({"error": f"Generation error: {exc}"}), 500

    # ---------------------------------------------------------------------
    # Design mode – works like the original "design" command.
    # ---------------------------------------------------------------------
    else:
        # Lazy load the design model if not already loaded.
        global model_design
        if model_design is None:
            model_design = load_model(MODEL_DESIGN, fix_mistral_regex=True)
        instruct = payload.get("instruct")
        try:
            results = list(
                model_design.generate_voice_design(
                    text=text,
                    language=language,
                    instruct=instruct,
                )
            )
        except Exception as exc:
            return jsonify({"error": f"Generation error: {exc}"}), 500

    if not results:
        return jsonify({"error": "No audio generated"}), 500

    # The result objects from mlx_audio have an ``audio`` attribute (numpy array).
    audio_np = results[0].audio
    # Write to a temporary WAV file – the caller expects raw bytes.
    # We'll use the utility to get a unique path inside a temporary folder.
    # Return audio bytes directly without writing to disk
    from flask import Response

    # Convert numpy array to bytes. Assuming the array is float32.
    audio_bytes = audio_np.tobytes()
    return Response(audio_bytes, mimetype="audio/wav")


@app.route("/health", methods=["GET"])
def health() -> Any:
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # Run on the same port the original MLX TTS provider used (8082).
    port = int(os.getenv("MLX_TTS_SIDE_CAR_PORT", "8082"))
    app.run(host="0.0.0.0", port=port)
