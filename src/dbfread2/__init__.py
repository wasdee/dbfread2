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

__version__ = version("dbfread2")

from .dbf import DBF  # noqa: F401
from .deprecated_dbf import open, read  # noqa: F401
from .exceptions import DBFNotFoundError, MissingMemoFileError  # noqa: F401
from .field_parser import FieldParser, InvalidValue  # noqa: F401

# Prevent star import.
__all__ = []
