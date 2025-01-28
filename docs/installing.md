# Installation

## Requirements

- Python 3.12 or later
- No external dependencies required - `dbfread2` is a pure Python module

## Installing with pip

```bash
pip install dbfread2
```

## Development Installation

For development, we recommend using [mise-en-place](https://mise.jdx.dev/) to manage Python versions and dependencies:

1. Install mise-en-place
2. Clone the repository:
   ```bash
   git clone https://github.com/wasdee/dbfread2.git
   cd dbfread2
   ```
3. Set up the development environment:
   ```bash
   mise install
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[docs]"
   ```
