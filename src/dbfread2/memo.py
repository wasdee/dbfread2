"""
Reads data from FPT (memo) files.

FPT files are used to store varying length text or binary data which is too
large to fit in a DBF field.

VFP == Visual FoxPro
DB3 == dBase III
DB4 == dBase IV
"""
from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from .ifiles import ifind
from .struct_parser import StructParser

VFPFileHeader = StructParser(
    'FPTHeader',
    '>LHH504s',
    ['nextblock',
     'reserved1',
     'blocksize',
     'reserved2'])

VFPMemoHeader = StructParser(
    'FoxProMemoHeader',
    '>LL',
    ['type',
     'length'])

DB4MemoHeader = StructParser(
    'DBase4MemoHeader',
    '<LL',
    ['reserved',  # Always 0xff 0xff 0x08 0x08.
     'length'])


class VFPMemo(bytes):
    """Base class for VFP memo fields."""
    pass


class BinaryMemo(VFPMemo):
    """Binary memo field."""
    pass


class PictureMemo(BinaryMemo):
    """Picture memo field."""
    pass


class ObjectMemo(BinaryMemo):
    """Object memo field."""
    pass


class TextMemo(VFPMemo):
    """Text memo field."""
    pass


VFP_TYPE_MAP: dict[int, type[VFPMemo]] = {
    0x0: PictureMemo,
    0x1: TextMemo,
    0x2: ObjectMemo,
}


class MemoFile:
    """Base class for memo file handlers."""

    def __init__(self, filename: str | Path) -> None:
        self.filename: str | Path = filename
        self.file: BinaryIO
        self._open()
        self._init()

    def _init(self) -> None:
        """Initialize memo file specific attributes."""
        pass

    def _open(self) -> None:
        """Open the memo file for reading."""
        self.file = open(self.filename, 'rb')
        # Shortcuts for speed
        self._read = self.file.read
        self._seek = self.file.seek

    def _close(self) -> None:
        """Close the memo file."""
        self.file.close()

    def __getitem__(self, index: int) -> bytes | None:
        """Get memo data at the specified index."""
        raise NotImplementedError

    def __enter__(self) -> MemoFile:
        return self

    def __exit__(self, type_, value, traceback) -> bool:
        self._close()
        return False


class FakeMemoFile(MemoFile):
    """A memo file that always returns None, used when no memo file exists."""

    def __getitem__(self, i: int) -> None:
        return None

    def _open(self) -> None:
        pass

    _init = _close = _open


class VFPMemoFile(MemoFile):
    """Visual FoxPro memo file handler."""

    def _init(self) -> None:
        self.header = VFPFileHeader.read(self.file)

    def __getitem__(self, index: int) -> VFPMemo | None:
        """Get a memo from the file."""
        if index <= 0:
            return None

        self._seek(index * self.header.blocksize)
        memo_header = VFPMemoHeader.read(self.file)

        data = self._read(memo_header.length)
        if len(data) != memo_header.length:
            raise OSError('EOF reached while reading memo')

        return VFP_TYPE_MAP.get(memo_header.type, BinaryMemo)(data)


class DB3MemoFile(MemoFile):
    """dBase III memo file handler."""

    def __getitem__(self, index: int) -> bytes | None:
        """Get a memo from the file."""
        if index <= 0:
            return None

        block_size = 512
        self._seek(index * block_size)
        data = b''

        while True:
            newdata = self._read(block_size)
            if not newdata:
                return data
            data += newdata

            # Find end of memo marker
            end_of_memo = data.find(b'\x1a')
            if end_of_memo != -1:
                return data[:end_of_memo]


class DB4MemoFile(MemoFile):
    """dBase IV memo file handler."""

    def __getitem__(self, index: int) -> bytes | None:
        """Get a memo from the file."""
        if index <= 0:
            return None

        block_size = 512
        self._seek(index * block_size)
        memo_header = DB4MemoHeader.read(self.file)
        data = self._read(memo_header.length)
        return data.split(b'\x1f', 1)[0]


def find_memofile(dbf_filename: str | Path) -> str | Path | None:
    """Find the corresponding memo file for a DBF file."""
    for ext in ['.fpt', '.dbt']:
        name = ifind(dbf_filename, ext=ext)
        if name:
            return name
    return None


def open_memofile(filename: str | Path, dbversion: int) -> MemoFile:
    """Open a memo file based on the file extension and DBF version."""
    if str(filename).lower().endswith('.fpt'):
        return VFPMemoFile(filename)
    elif dbversion == 0x83:
        return DB3MemoFile(filename)
    else:
        return DB4MemoFile(filename)
