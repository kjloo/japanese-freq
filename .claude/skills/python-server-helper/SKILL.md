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
1. **Route Creation**: Automatic blueprint registration
2. **Service Generation**: Business logic implementation
3. **Form Handling**: Validation class creation
4. **Test Scaffolding**: Unit test templates with mocks
5. **Dependency Management**: Injected services

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
- Unit tests using pytest/mocker
- Integration tests via `make server/test`
- Cover error handling patterns
- Enforce module structure
