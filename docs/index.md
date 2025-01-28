# dbfread2 - Read DBF Files with Python

DBF is a file format used by databases such dBase, Visual FoxPro, and FoxBase+. This library reads DBF files and returns the data as native Python data types for further processing. It is primarily intended for batch jobs and one-off scripts.

```python
from dbfread import DBF
for record in DBF('people.dbf'):
    print(record)
# {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)}
# {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}
```

## Features

- Pure Python implementation
- Support for Python 3.12+
- Returns data as native Python data types
- Memory efficient iteration
- Support for most common field types
- Support for pathlib.Path for all file operations

## Quick Links

- [Installation Guide](installing.md)
- [Introduction and Tutorial](introduction.md)
- [API Documentation](dbf_objects.md)
- [Field Types Reference](field_types.md)
- [Changelog](changes.md)
