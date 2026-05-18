## ADDED Requirements

### Requirement: YAML configuration file
The system SHALL read configuration from a `config.yaml` file using PyYAML, validated by Pydantic v2 models.

#### Scenario: Load default config
- **WHEN** `config.yaml` contains valid settings for all sections
- **THEN** the loader SHALL return a typed `Settings` object with `models`, `search`, `server`, `sandbox`, `memory`, `skills`, `persistence`, `agent`, and `observability` attributes

#### Scenario: Missing required field raises error
- **WHEN** `config.yaml` omits the `models` section
- **THEN** a Pydantic `ValidationError` SHALL be raised with a clear message

### Requirement: Config sections and models
Each config section SHALL have a corresponding Pydantic model:

#### Scenario: ModelConfig validates correctly
- **WHEN** parsing valid model config with `name`, `provider`, `model`, `base_url`, `api_key_env`
- **THEN** a `ModelConfig` instance SHALL be created without errors

#### Scenario: ModelConfig rejects missing fields
- **WHEN** parsing model config without `model` field
- **THEN** a `ValidationError` SHALL be raised

### Requirement: Environment variable override
Configuration values SHALL be overridable by environment variables loaded from `.env` via `python-dotenv`.

#### Scenario: API key loaded from environment
- **WHEN** `TAVILY_API_KEY` is set in `.env`
- **THEN** the config loader SHALL read it into `Settings.search` when constructing search tools

#### Scenario: Missing .env file does not crash
- **WHEN** no `.env` file exists
- **THEN** the config loader SHALL continue with sensible defaults or empty strings for optional values

### Requirement: config.example.yaml documents all settings
An example config file SHALL exist at the repository root documenting every configurable setting.

#### Scenario: Example config is loadable
- **WHEN** loading `config.example.yaml` with the config loader
- **THEN** no validation errors SHALL be raised (any placeholder values SHALL be valid)
