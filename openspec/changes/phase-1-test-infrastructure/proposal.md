## Why

当前已有 pytest 基础配置和导入验证测试，但缺乏结构化的测试基础设施：无共享 fixture、无覆盖度报告、无测试分类体系，且首个实质性测试用例（config 加载验证）已存在但无组织规范。需要建立标准化的测试基础，为后续所有模块开发提供质量保障。

## What Changes

- 创建 `conftest.py` 共享 fixture 层（临时配置、环境变量管理）
- 添加 pytest 覆盖度报告配置（`.coveragerc` + pytest-cov）
- 建立测试分类体系（单元/集成标记）
- 整理现有测试用例，提取共享工具函数
- 新增 agent 工厂模块的单元测试骨架（当前模块已建但无测试）
- 新增工具模块测试骨架
- 在 pyproject.toml 中固化测试相关配置

## Capabilities

### New Capabilities

- `test-infra`: 测试基础设施能力：共享 fixture、覆盖度报告、测试约定与分类体系
- `test-config`: 配置系统测试（完善现有用例，覆盖边界场景）
- `test-agent`: Agent 工厂单元测试骨架
- `test-tools`: 工具模块单元测试骨架

### Modified Capabilities

（无，当前无已有 specs）

## Impact

- 修改 `backend/pyproject.toml`：添加 pytest-cov 依赖和 [tool.coverage] 配置
- 新建 `backend/tests/conftest.py`：共享 fixture
- 新建 `backend/tests/test_agent.py`：Agent 测试骨架
- 新建 `backend/tests/test_tools.py`：工具测试骨架（占位）
- 修改 `backend/tests/test_config.py`：使用共享 fixture 重构
