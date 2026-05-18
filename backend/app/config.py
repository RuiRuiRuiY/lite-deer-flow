from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    name: str
    provider: str
    model: str
    base_url: str
    api_key_env: str


class SearchConfig(BaseModel):
    primary: str = "tavily"
    tavily_api_key_env: str = "TAVILY_API_KEY"
    fallback: str = "exa_search"


class ServerConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class SandboxConfig(BaseModel):
    type: str = "local_shell"
    virtual_mode: bool = True
    timeout: int = 120


class MemoryConfig(BaseModel):
    type: str = "agents_md"
    file: str = "AGENTS.md"


class SkillsConfig(BaseModel):
    paths: list[str] = ["backend/app/skills"]


class PersistenceConfig(BaseModel):
    checkpointer: str = "sqlite"
    db_path: str = "data/checkpoints.db"
    store: str = "memory"


class AgentConfig(BaseModel):
    recursion_limit: int = 50


class LangSmithConfig(BaseModel):
    enabled: bool = False


class ObservabilityConfig(BaseModel):
    langsmith: LangSmithConfig = Field(default_factory=LangSmithConfig)


class Settings(BaseModel):
    models: dict[str, ModelConfig]
    search: SearchConfig = Field(default_factory=SearchConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)
    sandbox: SandboxConfig = Field(default_factory=SandboxConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    skills: SkillsConfig = Field(default_factory=SkillsConfig)
    persistence: PersistenceConfig = Field(default_factory=PersistenceConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    observability: ObservabilityConfig = Field(default_factory=ObservabilityConfig)


def _normalize_path(p: str) -> str:
    return str(Path(p))


def load_config(path: str | Path = "config.yaml") -> Settings:
    from dotenv import load_dotenv

    load_dotenv()

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if raw is None:
        raise ValueError(f"Empty config file: {path}")

    if "paths" in raw.get("skills", {}):
        raw["skills"]["paths"] = [_normalize_path(p) for p in raw["skills"]["paths"]]

    return Settings.model_validate(raw)
