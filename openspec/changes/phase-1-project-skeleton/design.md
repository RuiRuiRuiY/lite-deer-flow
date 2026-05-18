## Context

Phase 1 establishes the foundation for Lite-DeerFlow — a lightweight AI research agent. The project needs a reproducible build system, configuration conventions, and quality tooling before any agent logic. The key constraint is Windows-local development with Git Bash shell.

## Goals / Non-Goals

**Goals:**
- uv-managed monorepo with Python 3.12+, dependency locking via `uv.lock`
- `backend/pyproject.toml` with FastAPI, deepagents, langchain-openai, langgraph-checkpoint-sqlite, Tavily, and dev tooling (ruff, mypy, pytest)
- YAML config system with Pydantic models for all sections (model, search, server, sandbox, memory, skills, persistence, agent, observability)
- `.gitignore` that excludes venv, cache dirs, and runtime data (`data/`)
- Env vars loaded from `.env` via `python-dotenv`, with `.env.example` as template
- `AGENTS.md` as DeepAgents-compatible manual memory file
- pytest with `asyncio_mode = auto`, ruff (lint + format), mypy basic mode
- No runtime agent or API logic — just scaffold

**Non-Goals:**
- Agent creation (`create_deep_agent`) or runtime — deferred to subsequent changes
- FastAPI routes or server startup — deferred
- Streamlit frontend — deferred
- Any actual test logic beyond verifying imports

## Decisions

- **uv over pip/venv**: 10–100x faster dependency resolution, built-in lockfile (`uv.lock`), single tool for venv + sync + run. `.python-version` pins the Python version for `uv sync` reproducibility.
- **Pydantic v2 for config**: Native YAML parsing via `PyYAML`, then validated with Pydantic `BaseModel`. Each config section gets a typed model (e.g., `ModelConfig`, `SearchConfig`), with a top-level `Settings` model. Reads from `config.yaml` at `backend/` root.
- **ruff over flake8 + isort + black**: Single binary, 100x faster, covers lint + format + import sorting. Config in `pyproject.tool.ruff`. Line length 120, standard ruleset.
- **mypy basic mode over strict**: Many deepagents/langchain SDK types are dynamic. `ignore_missing_imports` skips untyped 3rd-party modules. Strict mode deferred to Phase 3.
- **pytest-asyncio with `asyncio_mode = auto`**: Every test file can use `async def` without decorators, matching the async-first codebase.
- **`python-dotenv` for `.env` loading**: Standard approach, loaded at config init. Environment variables override YAML values for secrets.
- **Directory layout mirrors PRD exactly**: `backend/app/agent/`, `backend/app/gateway/`, `backend/app/tools/`, `backend/app/skills/` — all as stubs with `__init__.py`. Ready for Phase 2 wiring.

## Risks / Trade-offs

- **Windows path separator**: YAML paths use POSIX-style (`/`). The config loader normalizes with `pathlib.PurePosixPath` on read. Mitigation: test with actual Windows paths early.
- **uv Windows compatibility**: uv has excellent Windows support, but rare edge cases exist with symlinks in `.python-version`. Mitigation: lock to a tested Python version (3.12) via `uv python install`.
- **deepagents pre-release API**: All deepagents imports guarded behind try/except ImportError in stubs. Mitigation: version locked in pyproject.toml constraints.
