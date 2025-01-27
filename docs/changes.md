# Changelog

## 0.1.0 (2024-01-27)

### Added

- Initial fork from dbfread
- Full Python 3.12+ support
- Type hints throughout the codebase
- Support for `pathlib.Path` in all file operations
- Modern development tools:
  - ruff for linting and formatting
  - mypy for static type checking
  - mise-en-place for Python version management
  - uv for dependency management
- Material for MkDocs documentation

### Changed

- Removed deprecated `dbfread.open()` and `dbfread.read()`
- `DBF` class is no longer a subclass of `list`
- Improved error messages and type safety
- Updated all dependencies to latest versions
- Modernized codebase structure

### Removed

- Support for Python versions below 3.12
- `DeprecatedDBF` class
- Legacy compatibility layers

## Previous Versions

For changes in previous versions of the original dbfread library, please visit:
[dbfread changelog](https://github.com/olemb/dbfread/blob/master/CHANGELOG.rst)
