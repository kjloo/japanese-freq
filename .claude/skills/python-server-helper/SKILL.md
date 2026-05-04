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
- Validate changes with `make server/test`

### Testing Requirements
- Unit tests using pytest/mocker
- Integration tests via `make server/test`
- Cover error handling patterns
- Enforce module structure
