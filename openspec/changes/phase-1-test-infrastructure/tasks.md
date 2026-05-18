## 1. 测试依赖与配置

- [x] 1.1 在 `pyproject.toml` 的 `[project.optional-dependencies] dev` 中添加 `pytest-cov>=5.0.0`
- [x] 1.2 在 `pyproject.toml` 中添加 `[tool.coverage]` 配置：`source = ["app"]`、`report = { exclude_lines = ["pragma: no cover"] }`
- [x] 1.3 运行 `uv sync` 验证依赖解析

## 2. 共享 Fixture 层 (conftest.py)

- [x] 2.1 创建 `backend/tests/conftest.py`，注册 pytest 标记 `unit`、`integration`、`e2e`
- [x] 2.2 实现 `--run-e2e` 命令行选项（`pytest_addoption`）
- [x] 2.3 实现 `temp_config` fixture：创建临时 YAML 文件，返回 `Path`，teardown 自动清理
- [x] 2.4 实现 `test_settings` fixture：基于 `temp_config` 返回 `Settings` 实例
- [x] 2.5 实现 `env_sandbox` fixture：备份和恢复 `os.environ` 修改

## 3. 配置测试重构

- [x] 3.1 重构 `test_config.py`：使用 `temp_config` fixture 替换 `NamedTemporaryFile` 手动管理
- [x] 3.2 新增 `test_load_nonexistent_config()`：验证 `FileNotFoundError`
- [x] 3.3 新增 `test_load_empty_config()`：验证空 YAML 抛出 `ValueError`
- [x] 3.4 新增 `test_settings_defaults()`：验证可选字段的默认值
- [x] 3.5 运行 `uv run pytest tests/test_config.py -v` 验证全部通过

## 4. 测试骨架文件

- [x] 4.1 创建 `backend/tests/test_agent.py`：包含一个 `def test_agent_module_imports()` 验证 `app.agent` 可导入
- [x] 4.2 创建 `backend/tests/test_tools.py`：包含一个 `def test_tools_module_imports()` 验证 `app.tools` 可导入

## 5. 验证

- [x] 5.1 运行 `uv run ruff check app tests` — 无错误
- [x] 5.2 运行 `uv run ruff format --check app tests` — 格式正确
- [x] 5.3 运行 `uv run pytest -v` — 所有测试通过
- [x] 5.4 运行 `uv run pytest --cov=app --cov-report=term` — 覆盖度报告正常输出
