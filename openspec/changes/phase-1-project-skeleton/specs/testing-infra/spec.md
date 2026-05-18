## ADDED Requirements

### Requirement: pytest runs with asyncio support
The test framework SHALL support `async def` test functions without per-test decorators.

#### Scenario: Async test passes
- **WHEN** `uv run pytest` is executed in `backend/`
- **THEN** any `async def test_*` function SHALL execute without requiring `@pytest.mark.asyncio`

#### Scenario: pytest discovers tests
- **WHEN** `uv run pytest --co` is executed
- **THEN** test functions in `backend/tests/` SHALL be discovered

### Requirement: ruff enforces code style
All Python code SHALL pass `ruff check` with no errors for the configured rule set.

#### Scenario: ruff check passes on clean code
- **WHEN** `uv run ruff check backend/` is executed
- **THEN** it SHALL exit with code 0 on conforming code

#### Scenario: ruff format is consistent
- **WHEN** `uv run ruff format --check backend/` is executed
- **THEN** it SHALL exit with code 0 on well-formatted code

### Requirement: mypy type checks importable modules
The type checker SHALL run in basic mode, skipping untyped third-party libraries.

#### Scenario: mypy passes on stub modules
- **WHEN** `uv run mypy backend/app/` is executed
- **THEN** it SHALL exit with code 0
