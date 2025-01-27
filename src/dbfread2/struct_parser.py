"""
Parser that converts (C style) binary structs to dataclass instances.

The struct can be read from a file or a byte string.
"""

import struct
from dataclasses import dataclass
from typing import Any, BinaryIO, ClassVar, TypeVar

T = TypeVar('T', bound='StructBase')

@dataclass
class StructBase:
    """Base class for all struct classes."""
    _names: ClassVar[list[str]]

    def __repr__(self) -> str:
        fields = ', '.join(f'{name}={getattr(self, name)!r}'
                         for name in self._names)
        return f'{self.__class__.__name__}({fields})'


def _make_struct_class(name: str, names: list[str]) -> type[StructBase]:
    """Create a new dataclass type with the given name and field names.
    
    Args:
        name: Name of the new class
        names: List of field names for the struct
        
    Returns:
        A new dataclass type with the specified fields
    """
    fields = [(name, Any) for name in names]
    cls = dataclass(type(name, (StructBase,), {
        '__annotations__': {name: Any for name in names},
        '_names': names
    }))
    return cls


class StructParser:
    """Parser for C-style binary structs.
    
    Args:
        name: Name of the struct class to create
        format: Struct format string (see struct module documentation)
        names: List of field names corresponding to the struct format
    """

    def __init__(self, name: str, format: str, names: list[str]) -> None:
        self.format: str = format
        self.names: list[str] = names
        self.struct: struct.Struct = struct.Struct(format)
        self.Class: type[StructBase] = _make_struct_class(name, names)
        self.size: int = self.struct.size

    def unpack(self, data: bytes) -> StructBase:
        """Unpack struct from binary string and return a dataclass instance.
        
        Args:
            data: Binary data to unpack
            
        Returns:
            A dataclass instance containing the unpacked data
        """
        items = zip(self.names, self.struct.unpack(data), strict=True)
        return self.Class(**dict(items))

    def read(self, file: BinaryIO) -> StructBase:
        """Read struct from a file-like object (implementing read()).
        
        Args:
            file: Binary file-like object to read from
            
        Returns:
            A dataclass instance containing the read data
        """
        return self.unpack(file.read(self.struct.size))
