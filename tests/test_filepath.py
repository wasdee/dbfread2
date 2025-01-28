"""
Tests for file path handling.
"""
from pathlib import Path

from dbfread2 import DBF


def test_pathlib_path() -> None:
    """Test that pathlib.Path objects are supported."""
    # Using str path
    table_str = DBF('tests/cases/memotest.dbf')
    
    # Using pathlib.Path
    path = Path('tests/cases/memotest.dbf')
    table_path = DBF(path)
    
    # Both should work the same way
    assert len(table_str) == len(table_path)
    assert list(table_str) == list(table_path)
    
    # Verify the filename is stored correctly
    assert table_path.filename == str(path)
