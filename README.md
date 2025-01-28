# 📚 dbfread2

> 🚀 A modern Python library for reading DBF files with elegance and type safety

[![PyPI version](https://badge.fury.io/py/dbfread2.svg)](https://badge.fury.io/py/dbfread2)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`dbfread2` is a modern, type-safe Python library for reading DBF files (dBase, Visual FoxPro, FoxBase+) with zero external dependencies.

## ✨ Highlights

- 🐍 Modern Python 3.12+ implementation
- 🔍 Comprehensive type hints
- 🛠️ Simple yet powerful API
- 📁 Native `pathlib.Path` support
- 🔄 Streaming and memory-loaded modes
- 📝 Support for all major DBF variants
- 📋 18 field types with extensible `FieldParser`
- 📎 Reads `FPT` and `DBT` memo files
- 🔒 Type-safe operations

## 🚀 Quick Start

```python
from dbfread2 import DBF

# Stream records (memory-efficient)
for record in DBF('people.dbf'):
    print(record)
# {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)}
# {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}

# Load all records into memory
table = DBF('people.dbf', load=True)
print(table.records[0]['NAME'])  # Returns: 'Alice'
```

## 📦 Installation

```bash
pip install dbfread2
```

## 🔄 Migration from dbfread

### Key Changes

1. **Python Version**

   - ✅ Python 3.12+ required
   - ❌ No support for older versions

2. **Import Updates**

   ```python
   # Before ❌
   from dbfread import DBF
   # After ✅
   from dbfread2 import DBF
   ```

3. **Modern Parameter Names**

   ```python
   # Before ❌
   DBF('file.dbf', recfactory=dict, lowernames=True)
   # After ✅
   DBF('file.dbf', record_factory=dict, lowercase_names=True)
   ```

4. **Path Support**
   ```python
   # ✨ New Feature
   from pathlib import Path
   DBF(Path('data/file.dbf'))
   ```

## 🛠️ Development

### Setup

1. **Install Tools**

   - [mise-en-place](https://mise.jdx.dev/) for environment management
   - [uv](https://github.com/astral-sh/uv) for package management

2. **Clone & Setup**
   ```bash
   git clone https://github.com/wasdee/dbfread2.git
   cd dbfread2
   mise install
   uv pip install -e ".[docs]"
   ```

### 📚 Documentation

```bash
mise run docs:build    # Build docs
mise run docs:serve    # Serve locally
mise run docs:watch    # Watch mode
mise run docs:check    # Check for issues
```

### ✅ Code Quality

- 🧹 [ruff](https://github.com/astral-sh/ruff) - Linting & formatting
- 🔍 [mypy](https://mypy-lang.org/) - Static type checking

## 📄 License

MIT License

## 🙏 Credits

Fork of [dbfread](https://github.com/olemb/dbfread) by Ole Martin Bjørndalen

## 📬 Contact

Nutchanon Ninyawee - me@nutchanon.org

---

⭐️ If this project helps you, consider giving it a star!
