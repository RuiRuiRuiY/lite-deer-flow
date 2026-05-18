## ADDED Requirements

### Requirement: Monorepo directory layout
The system SHALL use a monorepo directory layout with `backend/`, `frontend/`, and `data/` as top-level directories.

#### Scenario: Directories exist after scaffold
- **WHEN** the project scaffold is created
- **THEN** the following directories MUST exist: `backend/app/agent/`, `backend/app/gateway/routers/`, `backend/app/tools/`, `backend/app/skills/research/`, `backend/app/skills/report/`, `frontend/`, `data/threads/`, `data/memories/`, `data/logs/`, `backend/tests/`

### Requirement: uv-managed Python dependencies
Dependencies MUST be managed with `uv`, with a `pyproject.toml` at `backend/` root and `.python-version` pinning Python 3.12.

#### Scenario: uv sync resolves dependencies
- **WHEN** running `uv sync --frozen` in the `backend/` directory
- **THEN** all dependencies SHALL resolve without errors and a virtual environment SHALL be created at `backend/.venv/`

#### Scenario: pyproject.toml contains expected tool config
- **WHEN** inspecting `backend/pyproject.toml`
- **THEN** it MUST contain `[project]` with dependencies, `[tool.ruff]`, `[tool.mypy]`, and `[tool.pytest.ini_options]` sections

### Requirement: .gitignore excludes build artifacts and runtime data
The `.gitignore` SHALL exclude virtual environments, cache directories, and runtime `data/` directory.

#### Scenario: gitignore covers all expected patterns
- **WHEN** reading `.gitignore`
- **THEN** it MUST contain entries for `.venv/`, `__pycache__/`, `.ruff_cache/`, `.mypy_cache/`, `data/`, and `.env`

### Requirement: Agent memory file exists
An `AGENTS.md` SHALL exist at the repository root with a standard memory format readable by DeepAgents.

#### Scenario: AGENTS.md is valid markdown
- **WHEN** reading `AGENTS.md`
- **THEN** it MUST contain `## 用户偏好` and `## 项目上下文` sections

### Requirement: All Python packages are importable
All created Python stub packages SHALL be valid Python packages with `__init__.py` files.

#### Scenario: Packages are importable
- **WHEN** running `python -c "import app; import app.agent; import app.gateway; import app.tools"`
- **THEN** no ImportError SHALL be raised
