# API Changes

## Changes from dbfread to dbfread2

### New Features

- Full Python 3.12+ support
- Type hints throughout the codebase
- Support for `pathlib.Path` in all file operations
- Modern development tools (ruff, mypy)
- Improved documentation with Material for MkDocs

### Breaking Changes

1. Removed deprecated functions:

   - `dbfread.open()`
   - `dbfread.read()`

2. `DBF` class is no longer a subclass of `list`

   - Cleaner and more explicit API
   - Better type safety
   - Migration example:

   ```python
   # Old code (dbfread)
   table = dbfread.read('people.dbf')
   print(table[1])  # Direct list access

   # New code (dbfread2)
   table = DBF('people.dbf', load=True)
   print(table.records[1])  # Explicit records access
   ```

### Compatibility Notes

- The `DeprecatedDBF` class has been removed
- All file operations now accept both strings and `pathlib.Path` objects
- Python versions below 3.12 are no longer supported

### Type Safety

dbfread2 includes comprehensive type hints:

```python
from dbfread2 import DBF
from pathlib import Path

# Both work
table1 = DBF('people.dbf')
table2 = DBF(Path('people.dbf'))

# Type hints for records
for record in table1:
    name: str = record['NAME']
    age: int = record['AGE']
```
