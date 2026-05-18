import os
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
import yaml

from app.config import ModelConfig, Settings


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "unit: Unit test (default)")
    config.addinivalue_line("markers", "integration: Integration test requiring dependencies")
    config.addinivalue_line("markers", "e2e: End-to-end test requiring external services")


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-e2e",
        action="store_true",
        default=False,
        help="Run end-to-end tests",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if not config.getoption("--run-e2e"):
        skip_e2e = pytest.mark.skip(reason="Use --run-e2e to include")
        for item in items:
            if "e2e" in item.keywords:
                item.add_marker(skip_e2e)


@pytest.fixture
def temp_config() -> Generator[Path, None, None]:
    config_data = {
        "models": {
            "primary": ModelConfig(
                name="test-model",
                provider="openai",
                model="gpt-4",
                base_url="https://api.openai.com/v1",
                api_key_env="TEST_KEY",
            ).model_dump(),
        }
    }
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as f:
        yaml.dump(config_data, f)
        tmp = Path(f.name)
    yield tmp
    tmp.unlink()


@pytest.fixture
def test_settings(temp_config: Path) -> Settings:
    from app.config import load_config

    return load_config(temp_config)


@pytest.fixture
def env_sandbox() -> Generator[None, None, None]:
    backup = dict(os.environ)
    yield
    os.environ.clear()
    os.environ.update(backup)
