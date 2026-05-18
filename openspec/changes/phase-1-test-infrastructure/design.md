## Context

当前 `backend/tests/` 仅有两个测试文件（`test_config.py`、`test_imports.py`），约 70 行代码，无共享 fixture、无覆盖度度量、无测试分类。随着后续 agent 工厂、网关路由、工具模块等代码的交付，需要建立可扩展的测试基础设施。

pyproject.toml 已配置：
- `pytest` + `pytest-asyncio`（asyncio_mode=auto）
- `testpaths = ["tests"]`
- ruff/mypy 已就绪

## Goals / Non-Goals

**Goals:**
- 建立 `conftest.py` 共享 fixture 层（临时文件/目录、配置对象、环境变量沙盒）
- 添加测试覆盖度报告（pytest-cov + `coverage` 配置）
- 定义测试分类标记体系（`unit`、`integration`、`e2e`）
- 重构 `test_config.py` 使用共享 fixture
- 为 agent、tools 模块创建测试骨架（含占位测试）
- 在 pyproject.toml 中固化所有测试相关配置

**Non-Goals:**
- 编写 agent 工厂的实质性测试（待 agent 代码实现后补充）
- 集成测试（需要真实 API key）
- CI/CD 流水线配置
- 性能/压力测试

## Decisions

1. **conftest.py 单文件 vs 多文件** → 单文件 `tests/conftest.py`。当前模块少，单文件可维护；后续模块增多时拆为 `tests/conftest/` 包。
2. **覆盖度工具** → `pytest-cov` 而非独立 `coverage run`。pytest-cov 与 pytest 集成更好，一条命令即可运行测试+生成报告。
3. **测试标记** → 内置 `pytest.mark` 而非自定义插件。`unit` 为默认标记，`integration` 需要显式标注，`e2e` 需要 `--run-e2e` 参数（`addoption`）。
4. **fixture 范围** → 函数级（`function`）为主。现阶段 fixture 轻量，无需 session/module 级缓存。

## Risks / Trade-offs

- [低风险] pytest-cov 增加 ~10% 测试执行时间 → 仅在 CI 或显式 `--cov` 时启用，本地开发默认不启用
- [低风险] fixture 过多可能降低可读性 → 限制 conftest.py 不超过 100 行，复杂 fixture 写在对应 test_ 文件头部
- [低风险] 测试标记不统一 → 在 conftest.py 中用 `register_markers` 注册并校验未知标记
