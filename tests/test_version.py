from importlib.metadata import version

import dbfread2


def test_version() -> None:
    """Test that __version__ is properly set from importlib.metadata."""
    expected = version("dbfread2")
    assert dbfread2.__version__ == expected
