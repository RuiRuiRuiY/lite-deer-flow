## Why

Lite-DeerFlow needs a solid foundation before any agent logic can be built. Without a proper monorepo structure, configuration system, and testing infrastructure, even simple changes risk breaking the project. This establishes the project skeleton so subsequent phases have clear conventions, reproducible builds, and verifiable quality.

## What Changes

- Create monorepo directory structure (`backend/`, `frontend/`, `data/`, root configs)
- Set up `backend/pyproject.toml` with uv-managed dependencies (FastAPI, langchain-openai, deepagents, langgraph-checkpoint-sqlite, uvicorn, Tavily, server-sent-events)
- Configure `ruff` (lint + format) and `mypy` (basic mode) in pyproject.toml
- Set up `pytest` with `pytest-asyncio` + `asyncio_mode = auto`
- Create `.python-version` for uv Python version pinning
- Add `.gitignore` for Python venv, cache dirs, and runtime data
- Create `config.example.yaml` with model, search, server, sandbox, memory, skills, persistence, agent, and observability sections
- Create `.env.example` with all required environment variable placeholders
- Create `AGENTS.md` manual memory file with default user preferences
- Add `README.md` with project description, quick start, and development commands
- Implement `backend/app/__init__.py` and stub `backend/app/main.py` as module marker
- Add `data/` directory structure with `.gitkeep` files for threads, checkpoints, memories, logs

## Capabilities

### New Capabilities
- `project-structure`: Monorepo scaffolding with uv-managed dependencies, ruff/mypy/pytest configuration, Python version pinning, and `.gitignore`
- `config-system`: YAML config loading with Pydantic models for model, search, server, sandbox, memory, skills, persistence, agent, and observability settings
- `testing-infra`: pytest + pytest-asyncio setup with `asyncio_mode = auto`, mypy basic type checking, and ruff lint/format rules

### Modified Capabilities

<!-- No existing capabilities to modify. -->

## Impact

- **Dependencies**: uv, Python 3.12+, FastAPI, uvicorn, deepagents, langchain-openai, langgraph-checkpoint-sqlite, Tavily, pyyaml, pydantic, pytest, pytest-asyncio, ruff, mypy
- **Code**: Creates the entire directory scaffold and root config files. No runtime agent logic yet.
- **Data**: `data/` directory tree for runtime data will be gitignored
