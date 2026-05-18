import tempfile
from pathlib import Path

import pytest
import yaml

from app.config import ModelConfig, Settings, load_config


def test_load_valid_config(temp_config: Path):
    cfg = load_config(temp_config)
    assert isinstance(cfg, Settings)
    assert cfg.models["primary"].model == "gpt-4"


def test_missing_models_raises(temp_config: Path):
    with open(temp_config, "w", encoding="utf-8") as f:
        yaml.dump({"server": {"host": "127.0.0.1"}}, f)
    with pytest.raises(Exception):
        load_config(temp_config)


def test_load_nonexistent_config():
    with pytest.raises(FileNotFoundError):
        load_config(Path("nonexistent_XXXXX.yaml"))


def test_load_empty_config():
    cfg_path = Path("tests/empty_test.yaml")
    try:
        cfg_path.write_text("", encoding="utf-8")
        with pytest.raises(ValueError):
            load_config(cfg_path)
    finally:
        cfg_path.unlink(missing_ok=True)


def test_settings_defaults():
    config_data = {
        "models": {
            "primary": {
                "name": "test",
                "provider": "openai",
                "model": "gpt-4",
                "base_url": "https://api.openai.com/v1",
                "api_key_env": "KEY",
            }
        }
    }
    tmp = Path(tempfile.mktemp(suffix=".yaml"))
    yaml.dump(config_data, open(tmp, "w", encoding="utf-8"))
    cfg = load_config(tmp)
    tmp.unlink()
    assert cfg.server.host == "127.0.0.1"
    assert cfg.server.port == 8000
    assert cfg.agent.recursion_limit == 50


def test_model_config_valid():
    mc = ModelConfig(
        name="test",
        provider="openai",
        model="gpt-4",
        base_url="https://api.openai.com/v1",
        api_key_env="TEST_KEY",
    )
    assert mc.model == "gpt-4"


def test_model_config_missing_field_raises():
    with pytest.raises(Exception):
        ModelConfig(
            name="test",
            provider="openai",
            base_url="https://api.openai.com/v1",
            api_key_env="TEST_KEY",
        )
