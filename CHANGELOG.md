# Changelog

All notable changes to ChimeraStack CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.2.0] – 2024-03-26

### Added

- JSON Schema validation for template.yaml files
- Jinja2-based template rendering pipeline
- Single canonical compose file strategy per stack
- Port allocation configuration via config/ports.yaml
- Component-specific post_copy tasks
- Comprehensive developer documentation
- Unit and integration tests with GitHub Actions

### Changed

- Standardized directory and naming conventions to kebab-case
- Migrated from string replacement to Jinja2 templating
- Flattened compose generation logic
- Improved cleanup mechanisms with per-component tasks

### Removed

- Legacy string replacement template processing
- Ad-hoc port allocation scanning
- Monolithic cleanup function
- Stray .override and .base compose files

### Fixed

- Port allocation conflicts through dedicated config
- Template validation with helpful error messages
- Component cleanup process reliability
- Documentation gaps for template authors

[v0.2.0]: https://github.com/amirofcodes/ChimeraStack-CLI/releases/tag/v0.2.0
