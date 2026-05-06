"""Utility functions for Qwen 3 TTS sidecar.
These are adapted from the standalone `tts/utils.py` repository.
"""

import os
import json
from pathlib import Path


def get_available_names(jsonl_path: str) -> list[str]:
    """Return a sorted list of unique speaker names in the dataset."""
    names = set()
    if os.path.exists(jsonl_path):
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except Exception:
                    continue
                if "name" in entry:
                    names.add(entry["name"])
    return sorted(names)


def get_available_labels_for_name(jsonl_path: str, name: str) -> list[str]:
    """Return sorted list of labels for a given speaker name."""
    labels = set()
    if os.path.exists(jsonl_path):
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except Exception:
                    continue
                if entry.get("name") == name and "label" in entry:
                    labels.add(entry["label"])
    return sorted(labels)


def load_reference_from_jsonl(jsonl_path: str, name: str, label: str) -> dict:
    """Find a reference entry matching name and label.

    Returns the JSON object with at least ``audio`` and ``text`` fields.
    Raises ``ValueError`` if not found.
    """
    if not os.path.exists(jsonl_path):
        raise ValueError(f"Dataset file not found: {jsonl_path}")
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except Exception:
                continue
            if entry.get("name") == name and entry.get("label") == label:
                return entry
    raise ValueError(f"No entry for name={name}, label={label} in {jsonl_path}")


def get_unique_path(directory: str, stem: str) -> Path:
    """Generate a unique WAV file path inside *directory* using *stem*.

    The function creates the directory if needed and appends a counter
    (e.g., ``speaker_japanese_01.wav``) to avoid overwriting existing files.
    """
    directory_path = Path(directory)
    directory_path.mkdir(parents=True, exist_ok=True)
    counter = 1
    while True:
        candidate = directory_path / f"{stem}_{counter:02d}.wav"
        if not candidate.exists():
            return candidate
        counter += 1
