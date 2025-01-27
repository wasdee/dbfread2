"""
Read DBF files with Python.

Example:

    >>> from dbfread2 import DBF
    >>> for record in DBF('people.dbf'):
    ...     print(record)
    {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)}
    {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}

Full documentation at https://dbfread.readthedocs.io/

"""
from importlib.metadata import version
from typing import Final

__version__: Final[str] = version("dbfread2")

from .dbf import DBF
from .exceptions import DBFNotFoundError, MissingMemoFileError
from .field_parser import FieldParser, InvalidValue

# Prevent star import.
__all__: Final[list[str]] = [
    "DBF",
    "DBFNotFoundError",
    "FieldParser",
    "InvalidValue",
    "MissingMemoFileError",
    "__version__",
]
