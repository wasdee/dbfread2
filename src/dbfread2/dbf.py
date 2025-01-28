"""
Class to read DBF files.
"""
from collections.abc import Callable
from datetime import date
from os import PathLike
from pathlib import Path
from typing import Any, BinaryIO, Union

from .codepages import guess_encoding
from .dbversions import get_dbversion_string
from .exceptions import DBFNotFoundError, MissingMemoFileError
from .field_parser import FieldParser
from .ifiles import ifind
from .memo import FakeMemoFile, find_memofile, open_memofile
from .struct_parser import StructParser

DBFHeader = StructParser(
    'DBFHeader',
    '<BBBBLHHHBBLLLBBH',
    ['dbversion',
     'year',
     'month',
     'day',
     'numrecords',
     'headerlen',
     'recordlen',
     'reserved1',
     'incomplete_transaction',
     'encryption_flag',
     'free_record_thread',
     'reserved2',
     'reserved3',
     'mdx_flag',
     'language_driver',
     'reserved4',
     ])

DBFField = StructParser(
    'DBFField',
    '<11scLBBHBBBB7sB',
    ['name',
     'type',
     'address',
     'length',
     'decimal_count',
     'reserved1',
     'workarea_id',
     'reserved2',
     'reserved3',
     'set_fields_flag',
     'reserved4',
     'index_field_flag',
     ])


def expand_year(year: int) -> int:
    """Convert 2-digit year to 4-digit year."""
    if year < 80:
        return 2000 + year
    else:
        return 1900 + year


class RecordIterator:
    """Iterator for DBF records."""

    def __init__(self, table: "DBF", record_type: bytes) -> None:
        self._record_type = record_type
        self._table = table

    def __iter__(self) -> Any:  # Returns iterator of records
        return self._table._iter_records(self._record_type)

    def __len__(self) -> int:
        return self._table._count_records(self._record_type)


class DBF:
    """DBF table."""

    def __init__(  # noqa: PLR0913
        self,
        filepath: str | PathLike[str],
        encoding: str | None = None,
        ignore_case: bool = True,
        lowercase_names: bool = False,
        parser_class: type[FieldParser] = FieldParser,
        record_factory: Callable[[list[tuple[str, Any]]], Any] | None = None,
        preload: bool = False,
        keep_raw: bool = False,
        ignore_missing_memo: bool = False,
        char_decode_errors: str = 'strict',
    ) -> None:
        """Initialize DBF table reader.

        Args:
            filepath: Path to the DBF file
            encoding: Character encoding of the DBF file
            ignore_case: Whether to ignore case in filename matching
            lowercase_names: Convert field names to lowercase
            parser_class: Class to use for parsing fields
            record_factory: Callable to create record objects (default: dict)
            preload: Whether to load all records into memory immediately
            keep_raw: Return raw bytes instead of parsed values
            ignore_missing_memo: Don't raise error if memo file is missing
            char_decode_errors: How to handle character decoding errors
        """
        self.encoding = encoding
        self.ignorecase = ignore_case
        self.lowernames = lowercase_names
        self.parserclass = parser_class
        self.raw = keep_raw
        self.ignore_missing_memofile = ignore_missing_memo
        self.char_decode_errors = char_decode_errors

        if record_factory is None:
            self.recfactory = lambda items: dict(items)
        else:
            self.recfactory = record_factory

        # Convert to Path object
        filepath = Path(filepath)
        # Name part before .dbf is the table name
        self.name = filepath.stem.lower()
        self._records: list[Any] | None = None
        self._deleted: list[Any] | None = None

        if ignore_case:
            self.filename = str(ifind(str(filepath)))
            if not self.filename:
                raise DBFNotFoundError(f'could not find file {filepath!r}')
        else:
            self.filename = str(filepath)

        # Filled in by self._read_headers()
        self.memofilename: str | None = None
        self.header: Any = None  # DBFHeader instance
        self.fields: list[Any] = []  # list of DBFField instances
        self.field_names: list[str] = []  # list of field names
        self.date: date | None = None

        with open(self.filename, mode='rb') as infile:
            self._read_header(infile)
            self._read_field_headers(infile)
            self._check_headers()

            try:
                self.date = date(expand_year(self.header.year),
                               self.header.month,
                               self.header.day)
            except ValueError:
                # Invalid date or '\x00\x00\x00'.
                self.date = None

        self.memofilename = self._get_memofilename()

        if preload:
            self.load()

    @property
    def dbversion(self) -> str:
        """Get the DBF version string."""
        return get_dbversion_string(self.header.dbversion)

    def _get_memofilename(self) -> str | None:
        """Get the memo filename if it exists."""
        # Does the table have a memo field?
        field_types = [field.type for field in self.fields]
        if not set(field_types) & set('MGPB'):
            # No memo fields.
            return None

        path = find_memofile(self.filename)
        if path is None:
            if self.ignore_missing_memofile:
                return None
            else:
                raise MissingMemoFileError(f'missing memo file for {self.filename}')
        else:
            return path

    @property
    def loaded(self) -> bool:
        """``True`` if records are loaded into memory."""
        return self._records is not None

    def load(self) -> None:
        """Load records into memory.

        This loads both records and deleted records. The ``records``
        and ``deleted`` attributes will now be lists of records.
        """
        if not self.loaded:
            self._records = list(self._iter_records(b' '))
            self._deleted = list(self._iter_records(b'*'))

    def unload(self) -> None:
        """Unload records from memory.

        The records and deleted attributes will now be instances of
        ``RecordIterator``, which streams records from disk.
        """
        self._records = None
        self._deleted = None

    @property
    def records(self) -> list[Any] | RecordIterator:
        """Records (not included deleted ones). When loaded a list of records,
        when not loaded a new ``RecordIterator`` object.
        """
        if self.loaded:
            return self._records
        else:
            return RecordIterator(self, b' ')

    @property
    def deleted(self) -> list[Any] | RecordIterator:
        """Deleted records. When loaded a list of records, when not loaded a
        new ``RecordIterator`` object.
        """
        if self.loaded:
            return self._deleted
        else:
            return RecordIterator(self, b'*')

    def _read_header(self, infile: BinaryIO) -> None:
        """Read the DBF header."""
        self.header = DBFHeader.read(infile)

        if self.encoding is None:
            try:
                self.encoding = guess_encoding(self.header.language_driver)
            except LookupError:
                self.encoding = 'ascii'

    def _decode_text(self, data: bytes) -> str:
        """Decode text using the specified encoding."""
        return data.decode(self.encoding or 'ascii', errors=self.char_decode_errors)

    def _read_field_headers(self, infile) -> None:
        """Read the field headers from the DBF file."""
        while True:
            sep = infile.read(1)
            if sep in (b'\r', b'\n', b''):
                # End of field headers
                break

            field = DBFField.unpack(sep + infile.read(DBFField.size - 1))

            field.type = chr(ord(field.type))

            # For character fields > 255 bytes the high byte
            # is stored in decimal_count.
            if field.type in 'C':
                field.length |= field.decimal_count << 8
                field.decimal_count = 0

            # Field name is b'\0' terminated.
            field.name = self._decode_text(field.name.split(b'\0')[0])
            if self.lowernames:
                field.name = field.name.lower()

            self.field_names.append(field.name)
            self.fields.append(field)

    def _open_memofile(self) -> Any:
        """Open the memo file if it exists."""
        if self.memofilename and not self.raw:
            return open_memofile(self.memofilename, self.header.dbversion)
        else:
            return FakeMemoFile(self.memofilename)

    def _check_headers(self) -> None:
        """Check headers for possible format errors."""
        field_parser = self.parserclass(self)

        for field in self.fields:
            if field.type == 'I' and field.length != 4:
                message = 'Field type I must have length 4 (was {})'
                raise ValueError(message.format(field.length))

            elif field.type == 'L' and field.length != 1:
                message = 'Field type L must have length 1 (was {})'
                raise ValueError(message.format(field.length))

            elif not field_parser.field_type_supported(field.type):
                raise ValueError(f'Unknown field type: {field.type!r}')

    def _skip_record(self, infile) -> None:
        """Skip a record in the DBF file."""
        # -1 for the record separator which was already read.
        infile.seek(self.header.recordlen - 1, 1)

    def _count_records(self, record_type: bytes = b' ') -> int:
        """Count the number of records of a given type."""
        count = 0

        with open(self.filename, 'rb') as infile:
            # Skip to first record.
            infile.seek(self.header.headerlen, 0)

            while True:
                sep = infile.read(1)
                if sep == record_type:
                    count += 1
                    self._skip_record(infile)
                elif sep in (b'\x1a', b''):
                    # End of records.
                    break
                else:
                    self._skip_record(infile)

        return count

    def _iter_records(self, record_type: bytes = b' ') -> Any:
        """Iterate over records of a given type."""
        with open(self.filename, 'rb') as infile, \
             self._open_memofile() as memofile:

            # Skip to first record.
            infile.seek(self.header.headerlen, 0)

            if self.raw:
                def parse(_, data):
                    return data
            else:
                field_parser = self.parserclass(self, memofile)
                parse = field_parser.parse

            # Shortcuts for speed.
            skip_record = self._skip_record
            read = infile.read

            while True:
                sep = read(1)

                if sep == record_type:
                    items = [
                        (field.name, parse(field, read(field.length)))
                        for field in self.fields
                    ]
                    yield self.recfactory(items)

                elif sep in (b'\x1a', b''):
                    # End of records.
                    break
                else:
                    skip_record(infile)

    def __iter__(self) -> Any:
        """Iterate over all records."""
        if self.loaded:
            return iter(self._records)
        else:
            return self._iter_records()

    def __len__(self) -> int:
        """Return the number of records."""
        return len(self.records)

    def __repr__(self) -> str:
        """Return a string representation of the DBF table."""
        status = 'loaded' if self.loaded else 'unloaded'
        return f'<{status} DBF table {self.filename!r}>'

    def __enter__(self) -> "DBF":
        """Context manager entry."""
        return self

    def __exit__(self, type_: Any, value: Any, traceback: Any) -> bool:
        """Context manager exit."""
        self.unload()
        return False
