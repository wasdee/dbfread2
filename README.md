# dbfread2 - Read DBF Files with Python

DBF is a file format used by databases such dBase, Visual FoxPro, and
FoxBase+. This library reads DBF files and returns the data as native
Python data types for further processing. It is primarily intended for
batch jobs and one-off scripts.

```python
from dbfread2 import DBF

for record in DBF('people.dbf'):
    print(record)
# {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)}
# {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}
```

By default records are streamed directly from the file. If you have
enough memory you can instead load them into a list for random access:

```python
table = DBF('people.dbf', load=True)
print(table.records[1]['NAME'])  # Returns: 'Bob'
print(table.records[0]['NAME'])  # Returns: 'Alice'
```

Full documentation at https://wasdee.github.io/dbfread2/

## Main Features

- Modern Python 3.12+ implementation
- Type hints throughout the codebase
- Simple but flexible API
- Data returned as native Python types
- Support for `pathlib.Path` in all file operations
- Records as dictionaries (customizable with record factories)
- Support for all major DBF variants
- 18 field types with extensible `FieldParser`
- Reads `FPT` and `DBT` memo files (text and binary)
- Case-insensitive file handling
- Access to deleted records

## Installation

Requires Python 3.12 or later.

```bash
pip install dbfread2
```

`dbfread2` is a pure Python module with no external runtime dependencies.

## Development

### Setup

We use [mise-en-place](https://mise.jdx.dev/) for development environment management:

1. Install mise-en-place
2. Clone and setup:

   ```bash
   git clone https://github.com/wasdee/dbfread2.git
   cd dbfread2
   mise install
   ```

3. Install dependencies with [uv](https://github.com/astral-sh/uv):
   ```bash
   uv pip install -e ".[docs]"
   ```

### Documentation

Documentation tasks are managed through mise:

```bash
# Build docs
mise run docs:build

# Serve docs locally (one-time)
mise run docs:serve

# Watch mode with auto-rebuild (recommended for development)
mise run docs:watch

# Check for documentation issues
mise run docs:check
```

### Code Quality

We use modern Python tools:

- [ruff](https://github.com/astral-sh/ruff) for linting and formatting
- [mypy](https://mypy-lang.org/) for static type checking

## License

dbfread2 is released under the MIT license.

## Credits

This is a fork of [dbfread](https://github.com/olemb/dbfread) by Ole Martin Bjørndalen.

## Contact

Nutchanon Ninyawee - me@nutchanon.org
