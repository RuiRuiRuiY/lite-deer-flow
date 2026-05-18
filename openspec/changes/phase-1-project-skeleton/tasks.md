## 1. Project Scaffold

- [x] 1.1 Create directory structure: `backend/app/agent/`, `backend/app/gateway/routers/`, `backend/app/tools/`, `backend/app/skills/research/`, `backend/app/skills/report/`, `frontend/`, `backend/tests/`, `data/threads/`, `data/memories/`, `data/logs/`, `data/checkpoints/`
- [x] 1.2 Create `.gitignore` with entries for `.venv/`, `__pycache__/`, `.ruff_cache/`, `.mypy_cache/`, `data/`, `.env`
- [x] 1.3 Create `.python-version` with `3.12`
- [x] 1.4 Create `.env.example` with placeholder vars: `DEEPSEEK_API_KEY`, `TAVILY_API_KEY`, `LANGSMITH_API_KEY`
- [x] 1.5 Create `README.md` with project description, quick start, and dev commands
- [x] 1.6 Add `.gitkeep` files to `data/` subdirectories

## 2. Python Package Scaffold

- [x] 2.1 Create `backend/pyproject.toml` with dependencies: fastapi, uvicorn[standard], deepagents, langchain-openai, langgraph-checkpoint-sqlite, tavily (langchain-tavily), python-dotenv, pyyaml, pydantic, httpx, sse-starlette
- [x] 2.2 Add dev dependencies to pyproject.toml: pytest, pytest-asyncio, ruff, mypy
- [x] 2.3 Configure [tool.ruff] in pyproject.toml: line-length=120, target-version=py312, select=["E","F","I","N","W","UP"], fixable=["I"]
- [x] 2.4 Configure [tool.mypy] in pyproject.toml: python_version=3.12, ignore_missing_imports=true, strict_optional=false
- [x] 2.5 Configure [tool.pytest.ini_options] in pyproject.toml: asyncio_mode="auto", testpaths=["tests"]
- [x] 2.6 Create `__init__.py` stubs in all `backend/app/` subpackages (agent, gateway, gateway/routers, tools, skills, skills/research, skills/report)
- [x] 2.7 Create `backend/app/main.py` with module-level docstring placeholder
- [x] 2.8 Run `uv sync` to generate `uv.lock` and verify dependencies resolve

## 3. Config System

- [x] 3.1 Create `config.example.yaml` with all sections: models (primary + fallback), search, server, sandbox, memory, skills, persistence, agent, observability — matching PRD Section 6.1
- [x] 3.2 Create `backend/app/config.py` with Pydantic models: `ModelConfig`, `SearchConfig`, `ServerConfig`, `SandboxConfig`, `MemoryConfig`, `SkillsConfig`, `PersistenceConfig`, `AgentConfig`, `ObservabilityConfig`, `Settings`
- [x] 3.3 Implement `load_config(path: str | Path = "config.yaml") -> Settings` function: reads YAML, validates with Pydantic, loads .env via python-dotenv
- [x] 3.4 Verify `config.example.yaml` is loadable by `load_config()` without validation errors

## 4. Agent Memory File

- [x] 4.1 Create `AGENTS.md` with `## 用户偏好` and `## 项目上下文` sections, populated with defaults from PRD Section 4.3

## 5. Testing Infra

- [x] 5.1 Create `backend/tests/__init__.py`
- [x] 5.2 Create `backend/tests/test_imports.py` verifying all packages are importable: `app`, `app.agent`, `app.gateway`, `app.tools`
- [x] 5.3 Create `backend/tests/test_config.py` with async tests: valid config loading, missing field raises ValidationError, ModelConfig validates correctly

## 6. Verification

- [x] 6.1 Run `uv run ruff check app tests` — must exit 0
- [x] 6.2 Run `uv run ruff format --check app tests` — must exit 0
- [x] 6.3 Run `uv run mypy app/` — must exit 0
- [x] 6.4 Run `uv run pytest` — all tests pass
