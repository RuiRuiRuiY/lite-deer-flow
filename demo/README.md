# Lite-DeerFlow Prototype

验证核心依赖能否协同工作，不涉及任何业务逻辑。

## 当前环境

| 依赖                        | 已验证版本 |
| --------------------------- | ---------- |
| Python                      | 3.13.12    |
| deepagents                  | 0.4.11     |
| langchain                   | 1.2.12     |
| langchain-core              | 1.2.22     |
| langgraph                   | 1.1.3      |
| langchain-openai            | 1.1.12     |
| langchain-tavily            | 0.2.17     |
| fastapi                     | 0.135.2    |
| streamlit                   | 1.55.0     |
| langgraph-checkpoint-sqlite | 3.1.0      |
| aiosqlite                   | 0.22.1     |

## 运行验证

```bash
python prototype.py
```

## 验证项

1. 所有核心包导入
2. `create_deep_agent` + subagents
3. `interrupt_on` + checkpointer
4. `with_fallbacks()`
5. `LocalShellBackend`
6. Tavily 工具
7. FastAPI + SSE 流式
8. Streamlit 基础
9. config.yaml 加载
10. AsyncSqliteSaver

## 版本约束

见 `pyproject.toml`，所有约束已通过 prototype 验证。
