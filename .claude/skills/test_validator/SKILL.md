version: 1.0

skill_name: test_validator

### Description
Skill for validating and enforcing testing standards across both the backend (Python/Pytest) and frontend (React/TypeScript/Vitest) in the Japanese frequency analyzer / partner chat project. This skill understands directory layouts, resource dependency management, client component test patterns, and execution commands for both unit and integration tests.

### Responsibilities
- **Server Validation:**
  - Validate that backend test files follow the established pattern in `server/test/`
  - Verify that server test resources (e.g., fixtures, mock datasets, sample media, JSON payloads) exist in `server/test/resources/`
  - Check that test output files are generated correctly in designated output/artifact directories
- **Client Validation:**
  - Enforce that modifications to any `.ts`/`.tsx` files under `client/src/` include corresponding test verification
  - Verify client test locations, co-located either under `client/src/components/__tests__/` or as `*.test.tsx` alongside components
  - Ensure client component mocks, socket handlers (Socket.IO), and API mocks (Axios) conform to project TypeScript interfaces
- **General Enforcement:**
  - Help activate appropriate test skills by confirming test structure compliance
  - Ensure test documentation aligns with project standards
  - Enforce clear architectural separation between unit test modules and integration test workflows

### Activation Conditions
This skill activates when:
- A server test file is added, modified, or reviewed in the `server/test/` directory
- A client file or test (`.ts`/`.tsx`) in `client/src/` is modified or reviewed
- Test resource files in `server/test/resources/` are created, updated, or referenced
- Unit or integration tests need structure validation
- Test execution commands or test documentation need review

### Integration & Execution Details

#### 1. Server Environment (Python / Pytest)
- **Test Location:** `server/test/test_*.py`
- **Test Resources:** `server/test/resources/<filename>`
- **Output Validation:** Check for expected generated output files/artifacts
- **Execution Command:** `pytest -vv server/test/<filename>_test.py` or `make test`

#### 2. Client Environment (React / Vitest)
- **Test Location:** Co-located in `client/src/components/__tests__/` or `client/src/**/*.test.tsx`
- **Testing Tech Stack:** Vitest + React Testing Library
- **Execution Command:** `make client/test` or `cd client && npm test`
- **Coverage Rule:** Any modification to components (e.g., `WelcomeCard`, `MineMenu`, `Chat`, `VideoPlayer`, `ProcessSettings`) or routes in `App.tsx` requires running client tests for validation.

---

### Key Concepts: Unit Tests vs. Integration Tests

Understanding the distinction between these two test scopes ensures proper test placement, mocking, and resource usage across both server and client domains:

#### 1. Unit Tests
* **Scope:** Test individual functions, isolated React components, or discrete server modules in isolation.
* **Client Application:** Render isolated React components (e.g., testing `WelcomeCard.tsx` props, state changes, or UI event handlers using Testing Library) with external dependencies (React Router, Axios, Socket.IO) stubbed out.
* **Server Application:** Test isolated Python logic without relying on external services, live databases, network endpoints, or physical disk artifacts. Mock or stub external API calls and heavy I/O.
* **Resource Usage:** Stubs and light fixtures loaded quickly into memory.
* **Speed & Execution:** Fast (milliseconds per test). Executed frequently during local development and continuous integration (CI) builds.

#### 2. Integration Tests
* **Scope:** Test how multiple components, pages, routing pathways, or end-to-end data processing pipelines work together.
* **Client Application:** Test full page workflows, lazy-loaded routes wrapped in `Suspense` inside `App.tsx`, complex form submissions across components, or multi-step WebSocket state flows.
* **Server Application:** Test multi-step server processing pipelines using realistic input resources from `server/test/resources/` and validating final generated outputs against expected schemas or artifacts.
* **Dependencies:** May interact with local databases, actual file structures, router histories, or mock server sockets mimicking full network connections.
* **Speed & Execution:** Slower (seconds to minutes). Typically executed before merging code or during full test suite runs.
