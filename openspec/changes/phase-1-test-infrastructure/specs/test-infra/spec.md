## ADDED Requirements

### Requirement: Shared test fixtures
The system SHALL provide shared pytest fixtures in `conftest.py` for common test needs.

#### Scenario: temp_config fixture provides isolated config
- **WHEN** a test uses the `temp_config` fixture
- **THEN** a temporary YAML file is created with the given config data
- **WHEN** the test completes
- **THEN** the temporary file is cleaned up

#### Scenario: test_settings fixture provides valid Settings object
- **WHEN** a test uses the `test_settings` fixture
- **THEN** a `Settings` instance with test defaults is returned

#### Scenario: env_sandbox fixture isolates environment variables
- **WHEN** a test uses the `env_sandbox` fixture
- **THEN** environment variable changes made during the test are reverted after the test

### Requirement: Test coverage reporting
The project SHALL support test coverage reporting via pytest-cov with configurable output.

#### Scenario: coverage report generation
- **WHEN** running `uv run pytest --cov=app --cov-report=term`
- **THEN** a coverage summary table is printed to stdout

#### Scenario: coverage configuration in pyproject.toml
- **WHEN** pytest-cov is invoked
- **THEN** coverage settings from `[tool.coverage]` in pyproject.toml are applied

### Requirement: Test classification markers
The project SHALL use pytest markers `unit`, `integration`, and `e2e` to classify tests.

#### Scenario: unit marker is default
- **WHEN** a test has no explicit marker
- **THEN** it is treated as a unit test

#### Scenario: e2e tests are opt-in
- **WHEN** running `uv run pytest`
- **THEN** tests marked `e2e` are skipped by default
- **WHEN** running `uv run pytest --run-e2e`
- **THEN** e2e tests are included
