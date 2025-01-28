"""
Functions for dealing with mixed-case files from case-preserving file
systems.

This module provides case-insensitive file operations for working with DBF and related files
across different case-sensitive and case-preserving filesystems.

Todo:

  - handle patterns that already have brackets
"""

import fnmatch
import glob
import os
from collections.abc import Iterator
from pathlib import Path
from typing import Union

PathLike = Union[str, Path]

def ipat(pat: PathLike) -> str:
    """Convert glob pattern to case insensitive form.
    
    Args:
        pat: A glob pattern to convert
        
    Returns:
        A case-insensitive version of the pattern
        
    Example:
        >>> ipat('test.dbf')
        '[Tt][Ee][Ss][Tt].[Dd][Bb][Ff]'
    """
    pat = str(pat)  # Convert Path to str if needed
    dirname, basename = os.path.split(pat)

    # Convert '/path/to/test.fpt' => '/path/to/[Tt][Ee][Ss][Tt].[Ff][Pp][Tt]'
    newpat = ''
    for char in basename:
        if char.isalpha():
            upper = char.upper()
            lower = char.lower()
            if upper != lower:
                newpat += f'[{upper}{lower}]'
            else:
                newpat += char
        else:
            newpat += char

    return str(Path(dirname) / newpat if dirname else newpat)


def ifnmatch(name: PathLike, pat: PathLike) -> bool:
    """Case insensitive version of fnmatch.fnmatch()
    
    Args:
        name: Filename to match against the pattern
        pat: Pattern to match against
        
    Returns:
        True if the name matches the pattern, False otherwise
    """
    return fnmatch.fnmatch(str(name), ipat(str(pat)))


def iglob(pat: PathLike) -> Iterator[str]:
    """Case insensitive version of glob.glob()
    
    Args:
        pat: Glob pattern to match against
        
    Returns:
        Iterator of matching filenames
    """
    return glob.glob(ipat(str(pat)))


def ifind(pat: PathLike, ext: str | None = None) -> str | None:
    """Look for a file in a case insensitive way.

    Args:
        pat: Pattern to search for
        ext: Optional extension to append to the pattern
        
    Returns:
        First matching filename if found, None otherwise
        
    Example:
        >>> ifind('test.dbf')
        'TEST.DBF'  # if TEST.DBF exists
        >>> ifind('test', ext='.dbf')
        'Test.DBF'  # if Test.DBF exists
    """
    pat = str(pat)
    if ext:
        pat = str(Path(pat).with_suffix(ext))

    files = list(iglob(pat))
    return files[0] if files else None


__all__ = ['ifind', 'ifnmatch', 'iglob', 'ipat']
