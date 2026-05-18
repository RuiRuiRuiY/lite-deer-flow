## ADDED Requirements

### Requirement: Config file not found handling
The system SHALL raise a clear error when the config file does not exist.

#### Scenario: missing config file raises FileNotFoundError
- **WHEN** `load_config("nonexistent.yaml")` is called
- **THEN** a `FileNotFoundError` is raised with the path in the message

### Requirement: Empty config file handling
The system SHALL raise a clear error when the config file is empty.

#### Scenario: empty YAML file raises ValueError
- **WHEN** `load_config()` is called on an empty YAML file
- **THEN** a `ValueError` is raised

### Requirement: Settings model defaults
The system SHALL provide sensible defaults for optional Settings fields.

#### Scenario: partial config uses defaults
- **WHEN** a config file contains only `models` and partial optional fields
- **THEN** the resulting `Settings` instance has defaults for all unspecified fields
- **AND** `Settings.server.host` defaults to `"127.0.0.1"`
- **AND** `Settings.server.port` defaults to `8000`
- **AND** `Settings.agent.recursion_limit` defaults to `50`

### Requirement: ModelConfig field validation
The system SHALL validate that ModelConfig has all required fields.

#### Scenario: missing model field raises ValidationError
- **WHEN** a ModelConfig is created without the `model` field
- **THEN** a `pydantic.ValidationError` is raised

#### Scenario: complete ModelConfig passes validation
- **WHEN** a ModelConfig is created with all required fields
- **THEN** the instance is valid and all fields are accessible
