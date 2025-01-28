# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-28

### Added

- Initial project setup as a fork of dbfread
- Support for Python 3.12 as target version
- Support for pathlib.Path in all file operations
- Comprehensive type hints throughout the codebase
- Ruff as the linter and formatter
- Mypy as the static type checker
- mise-en-place for Python version and package management
- GitHub Actions workflows for testing and documentation
- MkDocs with Material theme for documentation
- New custom exceptions for better error handling
- Enhanced memo file handling
- Improved character encoding support

### Changed

- New author: Nutchanon Ninyawee (me@nutchanon.org)
- Project renamed from dbfread to dbfread2
- Migrated from setup.py to pyproject.toml
- Switched from pip to uv for package management
- Renamed parameters for clarity:
  - `recfactory` → `record_factory`
  - `lowernames` → `lowercase_names`
  - `parserclass` → `parser_class`
- Improved error messages and type safety
- Enhanced documentation structure and content

### Removed

- Support for Python versions below 3.12
- All version guard code for older Python versions
- Deprecated functions and compatibility layers
- Legacy configuration files (.flake8, tox.ini)
- Old documentation format (RST files)
- MANIFEST.in in favor of pyproject.toml
- setup.py in favor of pyproject.toml

[0.1.0]: https://github.com/wasdee/dbfread2/releases/tag/v0.1.0
