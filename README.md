# Lite-DeerFlow

轻量级 AI 研究 Agent，基于 LangChain DeepAgents 构建。

## 快速开始

```bash
cd backend
uv sync
uv run pytest
```

## 开发命令

```bash
cd backend
uv run ruff check app/ tests/     # Lint
uv run ruff format --check app/ tests/  # Format check
uv run mypy app/                   # Type check
uv run pytest                      # Run tests
```

## 项目结构

```
backend/       # Python 后端 (FastAPI + DeepAgents)
frontend/      # Streamlit 前端
data/          # 运行时数据（gitignored）
  threads/     # 会话工作文件
  checkpoints/ # SQLite checkpointer
  memories/    # 跨线程记忆
  logs/        # 执行日志
```
