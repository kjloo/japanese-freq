"""Shared utilities for loading static test resources (audio, etc.)
used by integration tests. Mirrors the fixture pattern used by
client_fixture.py / mongo_fixture.py: import the fixture/helper you need
directly into your test module.
"""

from pathlib import Path
import pytest

# Anchored to this file's location so the path is correct regardless of
# which test module imports it or the pytest invocation cwd.
# server/test/fixture/resource_fixture.py -> parent.parent = server/test
RESOURCES_DIR = Path(__file__).resolve().parent.parent / "integration" / "resources"


def resource_path(*parts: str) -> Path:
    """
    Return the absolute Path to a file under test/integration/resources.

    Raises FileNotFoundError with a descriptive message if missing, so
    failures point directly at the expected location instead of a bare
    assertion.
    """
    path = RESOURCES_DIR / Path(*parts)
    if not path.is_file():
        raise FileNotFoundError(
            f"Test resource not found at {path}. "
            f"Expected resources under {RESOURCES_DIR}."
        )
    return path


@pytest.fixture
def resource_loader():
    """
    Fixture providing a callable to load integration test resource
    bytes by relative path segments.

    Usage:
        from test.fixture.resource_fixture import resource_loader

        def test_x(resource_loader):
            audio_bytes = resource_loader("audio", "stt_test.mp3")
    """

    def _load(*parts: str) -> bytes:
        return resource_path(*parts).read_bytes()

    return _load
