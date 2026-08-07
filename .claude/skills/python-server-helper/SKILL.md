version: 1.0

skill_name: python-server-helper

### Description
Server code generator for Flask architecture following project patterns. Automates implementation of:
- New API routes with proper blueprint registration
- Service layer implementations
- Form validation classes extending BaseForm
- Repository pattern data access
- Dependency injection setups
- Error handling patterns

### Generator Capabilities
1. **Route Creation**: Automatic blueprint registration with comprehensive test coverage
2. **Service Generation**: Business logic implementation with async operations
3. **Form Handling**: Validation class creation with comprehensive error handling
4. **Test Scaffolding**: Unit test templates with mocks for all dependencies
5. **Dependency Management**: Injected services with database connection management
6. **Test Audio Integration**: Creation of test audio fixtures for integration tests
7. **Output Validation**: Validation of generated test output files

### Guidelines
- Always extend BaseForm for validation
- Use repository pattern for data access
- Commit business logic to service layer
- Register blueprints in app_module.py
- Include mocks in tests
- When changing Python files, validate with `make server/test`

### Server Package Layout
- `main.py` – Flask app bootstrap and blueprint registration.
- `routes` – Blueprint modules exposing HTTP endpoints.
- `form` – Validation classes extending `BaseForm`.
- `service` – Business‑logic layer called by routes.
- `repository` – Data‑access layer (MongoDB) used by services.
- `mapper` – Functions translating between domain objects and JSON/Mongo formats.
- `model` – Domain model definitions.
- `util` – Helper utilities (logging, config, etc.).

#### Blueprint Registration
`server/app/main.py` imports `register_all_blueprints(app)` from `app/module/app_module.py`, which imports each blueprint from `app/routes/*` and registers them via `app.register_blueprint`.

```python
from app.module.app_module import app, register_all_blueprints
register_all_blueprints(app)
```

#### Form Structure
All form classes inherit from `BaseForm` (defined in `app/form/base_form.py`). Sub‑folders under `app/form`:
- `anki` – Anki card and settings forms
- `frequency` – Frequency analysis forms
- `llm` – LLM chat forms

Example form class:

```python
from app.form.base_form import BaseForm

class ExampleForm(BaseForm):
    field: str
```

### Example Code & Golden Files
Below are reference implementations (golden files) that illustrate how the core components are structured. Use them as templates when generating new modules.

- **Application bootstrap** – `server/app/main.py`
  ```python
  from app.module.app_module import app, register_all_blueprints

  # Register all blueprints (routes) with the Flask app
  register_all_blueprints(app)
  ```
- **Blueprint registration helper** – `server/app/module/app_module.py`
  Shows how each blueprint is imported and registered.

- **Route example** – `server/app/routes/word_routes.py`
  ```python
  from flask import Blueprint, jsonify, request
  from app.service import word_service

  word_routes = Blueprint("word_routes", __name__)

  @word_routes.route("/api/word/ignore-list/sync", methods=["POST"])
  def sync_ignore_list():
      data = request.get_json()
      word_service.update_from_anki(data["deck_id"], data["field_name"])
      return jsonify({"ignore_list": word_service.update_from_file()})
  ```
- **Base form definition** – `server/app/form/base_form.py`
  ```python
  from abc import ABC, abstractmethod

  class BaseForm(ABC):
      def __init__(self):
          self._validate()

      @abstractmethod
      def _validate(self):
          """Validate the form data."""
          pass
  ```
- **Service layer example** – `server/app/service/word_service.py`
  Demonstrates interaction with gateways, repositories, and socket notifications.

- **Repository example** – `server/app/repository/word/word_repository.py`
  Shows MongoEngine‑based data access patterns.

- **Gateway example** – `server/app/gateway/llm/llm_gateway.py`
  Provides a thin wrapper around the configured LLM provider.

Use these files as “golden” references when extending the codebase with new routes, services, forms, or repositories. The patterns (blueprint registration, BaseForm inheritance, repository usage) are consistent throughout the project.

### Testing Requirements
- Unit tests using pytest/mocker with database mock integration
- Integration tests via `make server/test` that include:
  - MongoDB connection mocks
  - Schema initialization for test data
  - Connection failure handling
- Test environment setup including:
  - Local MongoDB instance (`sudo service mongod restart`)
  - Test database initialization
- TDD patterns:
  - Fail-first tests for new features
  - Mock-based dependency isolation
- Test organization:
  - Mirror main code structure in `server/app/tests`
  - Fixtures for database contexts
- Required test components for database-enabled modules:
  - Mocked database connections
  - Test fixture for collections
  - Validation of schema changes

### New Fixtures to Implement
- `mocked_db_setup` fixture for initializing test collections
- `mock_collection` fixture for sample data
- Error handling fixtures for connection failures
- Database connection Teardown fixture

### Test Script Modifications
- Add `import pymongo` for connection utilities
- Implement retry logic for unstable connections
- Add test assertions for schema validation
- Include test output validation (e.g., `output.mp3` generation)

### Execution Guidance
- Test database initialization: `make server/test`
- Validate test audio location: `server/test/integration/resources/audio/stt_test.mp3`
- Verify output.mp3 generation:
  ```bash
  ls server/output/output.mp3
  ffplay server/output/output.mp3
  ```
- **Test Pattern**: After implementing a new feature, create a test file `server/test/<module>_test.py` that validates end-to-end functionality
- **Test Audio**: Put test audio at `server/test/integration/resources/audio/<filename>.mp3` for integration tests
- **Validation**: All new tests should be integrated with existing pytest configuration
- **Status**: Run tests via `make server/test` or `make test`

### Example Test Structure
```python
# server/test/integration/speech/test_speech_integration.py
import pytest
from pathlib import Path
from app.gateway.speech import transcribe, synthesize
from app.assistant.conversation_assistant import ConversationAssistant
from test.fixture.resource_fixture import resource_loader

def test_speech_pipeline_with_mocks(
    mock_conversation_assistant, mock_speech_gateway, mock_mongodb, resource_loader
):
    """Integration test: STT → Assistant → TTS pipeline"""
    mock_stt, mock_tts = mock_speech_gateway

    # Load test audio using the shared resource loader
    audio_bytes = resource_loader("audio", "stt_test.mp3")
    
    # 1. STT test
    stt_result = mock_stt(audio_bytes)
    
    # 2. Assistant test  
    assistant_response = mock_conversation_assistant.process(stt_result)
    
    # 3. TTS test
    tts_audio = mock_tts(assistant_response["speak"], language="Japanese")
    
    assert tts_audio == b"fake audio bytes"
    print("\n✅  Integration test passed!")
```

### Shared Resource Loading
Tests now use a centralized resource loading pattern via `test.fixture.resource_fixture`:

```python
# Inside test fixture (server/test/fixture/resource_fixture.py)
from pathlib import Path
import pytest

RESOURCES_DIR = Path(__file__).resolve().parent.parent / "integration" / "resources"

def resource_path(*parts: str) -> Path:
    """Return absolute path to a resource file under test/integration/resources."""
    path = RESOURCES_DIR / Path(*parts)
    if not path.is_file():
        raise FileNotFoundError(f"Test resource not found at {path}")
    return path

@pytest.fixture
def resource_loader():
    """Fixture providing callable to load resource bytes by path segments."""
    def _load(*parts: str) -> bytes:
        return resource_path(*parts).read_bytes()
    return _load
```

This centralized approach eliminates hardcoded paths and provides consistent resource loading across integration tests.
