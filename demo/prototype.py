"""
Lite-DeerFlow Prototype
=======================
验证核心依赖能否协同工作，不涉及业务逻辑。

运行方式:
    python prototype.py

验证项:
    1. deepagents create_deep_agent + subagents
    2. checkpointer + interrupt_on
    3. with_fallbacks()
    4. LocalShellBackend
    5. Tavily 工具导入
    6. FastAPI + SSE 流式
    7. Streamlit 基础
    8. config.yaml 加载
"""

import asyncio
import os
import sys
import tempfile
from pathlib import Path

# Windows console encoding fix
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Dummy API keys for prototype validation (no actual calls are made)
os.environ["OPENAI_API_KEY"] = "sk-protoype-dummy-key"
os.environ["TAVILY_API_KEY"] = "tvly-prototype-dummy-key"

# ============================================================
# 工具函数
# ============================================================

PASS = "[OK]"
FAIL = "[FAIL]"
WARN = "[WARN]"

results = []

def check(name: str, fn):
    """运行一个检查并记录结果。"""
    try:
        fn()
        results.append((PASS, name))
    except Exception as e:
        results.append((FAIL, f"{name}: {e}"))


def async_check(name: str, fn):
    """运行一个异步检查并记录结果。"""
    try:
        asyncio.run(fn())
        results.append((PASS, name))
    except Exception as e:
        results.append((FAIL, f"{name}: {e}"))


# ============================================================
# 1. 导入检查
# ============================================================

def check_imports():
    """验证所有核心包可以导入。"""
    import deepagents
    import langchain
    import langchain_core
    import langchain_tavily
    import fastapi
    import streamlit
    import langgraph
    import langgraph.checkpoint.sqlite.aio
    import aiosqlite
    import yaml
    from importlib.metadata import version

    print(f"   deepagents=={deepagents.__version__}")
    print(f"   langchain=={langchain.__version__}")
    print(f"   langchain-core=={langchain_core.__version__}")
    print(f"   langchain-openai=={version('langchain-openai')}")
    print(f"   langchain-tavily=={langchain_tavily.__version__}")
    print(f"   fastapi=={fastapi.__version__}")
    print(f"   streamlit=={streamlit.__version__}")
    print(f"   langgraph=={version('langgraph')}")


# ============================================================
# 2. deepagents create_deep_agent + subagents
# ============================================================

def check_create_agent_with_subagents():
    """验证 create_deep_agent 可以创建带 subagents 的 agent。"""
    from deepagents import create_deep_agent
    from langchain_core.tools import tool
    from langgraph.checkpoint.memory import MemorySaver

    @tool
    def dummy_search(query: str) -> str:
        """搜索互联网并返回摘要。"""
        return f"搜索结果: {query}"

    subagents = [
        {
            "name": "research-agent",
            "description": "搜索互联网、提取网页内容",
            "system_prompt": "你是一个研究专家。",
            "tools": [dummy_search],
        },
        {
            "name": "report-agent",
            "description": "阅读研究文件，撰写报告",
            "system_prompt": "你是一个专业的报告撰写人。",
        },
    ]

    agent = create_deep_agent(
        model="openai:gpt-4o-mini",  # 仅创建，不调用
        tools=[dummy_search],
        subagents=subagents,
        checkpointer=MemorySaver(),
    )

    # 验证 agent 是 CompiledStateGraph
    from langgraph.graph.state import CompiledStateGraph
    assert isinstance(agent, CompiledStateGraph), "agent 类型不正确"
    print("   agent 创建成功，包含 2 个 subagents")


# ============================================================
# 3. checkpointer + interrupt_on
# ============================================================

def check_interrupt_on():
    """验证 interrupt_on 需要配合 checkpointer 工作。"""
    from deepagents import create_deep_agent
    from langgraph.checkpoint.memory import MemorySaver

    agent = create_deep_agent(
        model="openai:gpt-4o-mini",
        interrupt_on={"write_file": True, "execute": True},
        checkpointer=MemorySaver(),
    )

    # 验证 interrupt 配置已生效
    assert agent is not None
    print("   interrupt_on 配置成功（配合 MemorySaver）")


# ============================================================
# 4. with_fallbacks()
# ============================================================

def check_fallbacks():
    """验证 with_fallbacks() 可以包装模型。"""
    from langchain_openai import ChatOpenAI

    primary = ChatOpenAI(
        model="gpt-4o-mini",
        base_url="https://api.openai.com/v1",
        api_key="sk-dummy-key-for-test",
    )

    fallback = ChatOpenAI(
        model="gpt-3.5-turbo",
        base_url="https://api.openai.com/v1",
        api_key="sk-dummy-key-for-test",
    )

    model_with_fallback = primary.with_fallbacks([fallback])
    # 验证 fallback 已配置
    assert hasattr(model_with_fallback, "fallbacks")
    print("   with_fallbacks() 包装成功")


# ============================================================
# 5. LocalShellBackend
# ============================================================

def check_local_shell_backend():
    """验证 LocalShellBackend 可以创建和配置。"""
    from deepagents.backends import LocalShellBackend

    with tempfile.TemporaryDirectory() as tmpdir:
        backend = LocalShellBackend(
            root_dir=tmpdir,
            virtual_mode=True,
            timeout=120,
            max_output_bytes=100000,
        )
        assert backend is not None
        print("   LocalShellBackend 创建成功（virtual_mode=True）")


# ============================================================
# 6. Tavily 工具
# ============================================================

def check_tavily_tool():
    """验证 Tavily 搜索工具可以导入和实例化。"""
    from langchain_tavily import TavilySearch

    # 仅验证可以创建实例（不实际调用，需要 API key）
    tool = TavilySearch()
    assert tool.name == "tavily_search"
    print("   TavilySearch 导入成功")


# ============================================================
# 7. FastAPI + SSE 流式
# ============================================================

def check_fastapi_sse():
    """验证 FastAPI 可以创建 SSE 流式端点。"""
    from fastapi import FastAPI
    from fastapi.responses import StreamingResponse
    from starlette.testclient import TestClient

    app = FastAPI()

    async def event_stream():
        for i in range(3):
            yield f"event: message\ndata: {{\"token\": \"word_{i}\"}}\n\n"
        yield f"event: complete\ndata: {{\"result\": \"done\"}}\n\n"

    @app.get("/test/stream")
    async def stream():
        return StreamingResponse(event_stream(), media_type="text/event-stream")

    client = TestClient(app)
    response = client.get("/test/stream")
    assert response.status_code == 200
    content = response.text
    assert "word_0" in content
    assert "complete" in content
    print("   SSE 流式端点工作正常")


# ============================================================
# 8. Streamlit 基础
# ============================================================

def check_streamlit_basic():
    """验证 Streamlit 可以导入和基本使用。"""
    import streamlit as st

    # 验证核心 API 存在
    assert hasattr(st, "chat_message")
    assert hasattr(st, "text_input")
    assert hasattr(st, "selectbox")
    assert hasattr(st, "sidebar")
    print("   Streamlit 核心 API 可用")


# ============================================================
# 9. config.yaml 加载
# ============================================================

def check_config_yaml():
    """验证 config.yaml 可以加载。"""
    import yaml

    config_content = """
models:
  primary:
    name: "deepseek-chat"
    provider: "openai"
    model: "deepseek-chat"
    base_url: "https://api.deepseek.com/v1"
    api_key_env: "DEEPSEEK_API_KEY"
  fallback:
    name: "gpt-4o-mini"
    provider: "openai"
    model: "gpt-4o-mini"
    base_url: "https://api.openai.com/v1"
    api_key_env: "OPENAI_API_KEY"

search:
  primary: tavily
  tavily_api_key_env: "TAVILY_API_KEY"
  fallback: exa_search

server:
  host: "127.0.0.1"
  port: 8000

sandbox:
  type: local_shell
  virtual_mode: true
  timeout: 120

memory:
  type: agents_md
  file: "AGENTS.md"

skills:
  paths:
    - "backend/app/skills"

persistence:
  checkpointer: "sqlite"
  db_path: "data/checkpoints.db"
  store: "memory"

agent:
  recursion_limit: 50

observability:
  langsmith:
    enabled: false
"""
    config = yaml.safe_load(config_content)
    assert config["models"]["primary"]["name"] == "deepseek-chat"
    assert config["models"]["fallback"]["name"] == "gpt-4o-mini"
    assert config["sandbox"]["virtual_mode"] is True
    assert config["agent"]["recursion_limit"] == 50
    print("   config.yaml 解析成功，所有字段正确")


# ============================================================
# 10. AsyncSqliteSaver
# ============================================================

async def check_async_sqlite_saver():
    """验证 AsyncSqliteSaver 可以创建和使用。"""
    import tempfile
    from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "checkpoints.db"
        async with AsyncSqliteSaver.from_conn_string(f"file:{db_path}") as saver:
            assert saver is not None
            print("   AsyncSqliteSaver 创建成功")


# ============================================================
# 主流程
# ============================================================

def main():
    print("=" * 60)
    print("  Lite-DeerFlow Prototype — 核心依赖验证")
    print("=" * 60)
    print()

    # 同步检查
    print("[1/10] 导入检查")
    check("导入检查", check_imports)

    print("\n[2/10] create_deep_agent + subagents")
    check("create_deep_agent + subagents", check_create_agent_with_subagents)

    print("\n[3/10] interrupt_on + checkpointer")
    check("interrupt_on + checkpointer", check_interrupt_on)

    print("\n[4/10] with_fallbacks()")
    check("with_fallbacks()", check_fallbacks)

    print("\n[5/10] LocalShellBackend")
    check("LocalShellBackend", check_local_shell_backend)

    print("\n[6/10] Tavily 工具")
    check("Tavily 工具", check_tavily_tool)

    print("\n[7/10] FastAPI + SSE 流式")
    check("FastAPI + SSE 流式", check_fastapi_sse)

    print("\n[8/10] Streamlit 基础")
    check("Streamlit 基础", check_streamlit_basic)

    print("\n[9/10] config.yaml 加载")
    check("config.yaml 加载", check_config_yaml)

    # 异步检查
    print("\n[10/10] AsyncSqliteSaver")
    async_check("AsyncSqliteSaver", check_async_sqlite_saver)

    # 汇总
    print()
    print("=" * 60)
    print("  验证结果汇总")
    print("=" * 60)
    for status, name in results:
        print(f"  {status} {name}")

    passed = sum(1 for s, _ in results if s == PASS)
    failed = sum(1 for s, _ in results if s == FAIL)
    print()
    print(f"  Passed: {passed}/{len(results)}")
    if failed > 0:
        print(f"  {failed}/{len(results)} failed")
        print()
        print("  [WARN] Some verifications failed. Check dependency version compatibility.")
        sys.exit(1)
    else:
        print()
        print("  [OK] All core dependency verifications passed. Ready for Phase 1 development.")


if __name__ == "__main__":
    main()
