"""
Parser for DBF fields.
"""
from __future__ import annotations

import datetime
import struct
from collections.abc import Callable
from decimal import Decimal
from typing import Any

from .memo import BinaryMemo


class InvalidValue(bytes):
    def __repr__(self) -> str:
        text = bytes.__repr__(self)
        return f'InvalidValue({text})'


class FieldParser:
    def __init__(self, table: Any, memofile: Any | None = None) -> None:
        """Create a new field parser

        encoding is the character encoding to use when parsing strings.
        """
        self.table = table
        self.dbversion = self.table.header.dbversion
        self.encoding = table.encoding
        self.char_decode_errors = table.char_decode_errors
        self._lookup: dict[str, Callable] = self._create_lookup_table()
        if memofile:
            self.get_memo = memofile.__getitem__
        else:
            self.get_memo = lambda x: None

    def decode_text(self, text: bytes) -> str:
        return str(text, self.encoding, errors=self.char_decode_errors)

    def _create_lookup_table(self) -> dict[str, Callable]:
        """Create a lookup table for field types."""
        lookup: dict[str, Callable] = {}

        for name in dir(self):
            if name.startswith('parse'):
                field_type = name[5:]
                if len(field_type) == 1:
                    lookup[field_type] = getattr(self, name)
                elif len(field_type) == 2:
                    # Hexadecimal ASCII code for field name.
                    # Example: parse2B() ('+' field)
                    field_type = chr(int(field_type, 16))
                    lookup[field_type] = getattr(self, name)

        return lookup

    def field_type_supported(self, field_type: str) -> bool:
        """Checks if the field_type is supported by the parser

        field_type should be a one-character string like 'C' and 'N'.
        Returns a boolen which is True if the field type is supported.
        """
        return field_type in self._lookup

    def parse(self, field: Any, data: bytes) -> Any:
        """Parse field and return value"""
        try:
            func = self._lookup[field.type]
        except KeyError as e:
            raise ValueError(f'Unknown field type: {field.type!r}') from e
        else:
            return func(field, data)

    def parse0(self, field: Any, data: bytes) -> bytes:
        """Parse flags field and return as byte string"""
        return data

    def parseC(self, field: Any, data: bytes) -> str:
        """Parse char field and return unicode string"""
        return self.decode_text(data.rstrip(b'\0 '))

    def parseD(self, field: Any, data: bytes) -> datetime.date | None:
        """Parse date field and return datetime.date or None"""
        try:
            return datetime.date(int(data[:4]), int(data[4:6]), int(data[6:8]))
        except ValueError as e:
            if data.strip(b' 0\0') == b'':
                # A record containing only spaces and/or zeros is
                # a NULL value.
                return None
            else:
                raise ValueError(f'invalid date {data!r}') from e

    def parseF(self, field: Any, data: bytes) -> float | None:
        """Parse float field and return float or None"""
        # In some files * is used for padding.
        data = data.strip().strip(b'*')

        if data:
            return float(data)
        else:
            return None

    def parseI(self, field: Any, data: bytes) -> int:
        """Parse integer or autoincrement field and return int."""
        return struct.unpack('<i', data)[0]

    def parseL(self, field: Any, data: bytes) -> bool | None:
        """Parse logical field and return True, False or None"""
        if data in b'TtYy':
            return True
        elif data in b'FfNn':
            return False
        elif data in b'? \0':
            return None
        else:
            message = 'Illegal value for logical field: {!r}'
            raise ValueError(message.format(data))

    def _parse_memo_index(self, data: bytes) -> int:
        if len(data) == 4:
            return struct.unpack('<I', data)[0]
        else:
            try:
                return int(data)
            except ValueError as e:
                if data.strip(b' \x00') == b'':
                    return 0
                else:
                    raise ValueError(
                        f'Memo index is not an integer: {data!r}') from e

    def parseM(self, field: Any, data: bytes) -> str | BinaryMemo | None:
        """Parse memo field (M, G, B or P)

        Returns memo index (an integer), which can be used to look up
        the corresponding memo in the memo file.
        """
        memo = self.get_memo(self._parse_memo_index(data))
        # Visual FoxPro allows binary data in memo fields.
        # These should not be decoded as string.
        if isinstance(memo, BinaryMemo):
            return memo
        elif memo is None:
            return None
        else:
            return self.decode_text(memo)

    def parseN(self, field: Any, data: bytes) -> int | float | None:
        """Parse numeric field (N)

        Returns int, float or None if the field is empty.
        """
        # In some files * is used for padding.
        data = data.strip().strip(b'*\0')

        try:
            return int(data)
        except ValueError:
            if not data.strip():
                return None
            else:
                # Account for , in numeric fields
                return float(data.replace(b',', b'.'))

    def parseO(self, field: Any, data: bytes) -> float:
        """Parse long field (O) and return float."""
        return struct.unpack('d', data)[0]

    def parseT(self, field: Any, data: bytes) -> datetime.datetime | None:
        """Parse time field (T)

        Returns datetime.datetime or None"""
        # Julian day (32-bit little endian)
        # Milliseconds since midnight (32-bit little endian)
        #
        # "The Julian day or Julian day number (JDN) is the number of days
        # that have elapsed since 12 noon Greenwich Mean Time (UT or TT) on
        # Monday, January 1, 4713 BC in the proleptic Julian calendar
        # 1. That day is counted as Julian day zero. The Julian day system
        # was intended to provide astronomers with a single system of dates
        # that could be used when working with different calendars and to
        # unify different historical chronologies." - wikipedia.org

        # Offset from julian days (used in the file) to proleptic Gregorian
        # ordinals (used by the datetime module)
        offset = 1721425  # Todo: will this work?

        if data.strip():
            # Note: if the day number is 0, we return None
            # I've seen data where the day number is 0 and
            # msec is 2 or 4. I think we can safely return None for those.
            # (At least I hope so.)
            day, msec = struct.unpack('<LL', data)
            if day:
                dt = datetime.datetime.fromordinal(day - offset)
                delta = datetime.timedelta(seconds=msec / 1000)
                return dt + delta
            else:
                return None
        else:
            return None

    def parseY(self, field: Any, data: bytes) -> Decimal:
        """Parse currency field (Y) and return decimal.Decimal.

        The field is encoded as a 8-byte little endian integer
        with 4 digits of precision."""
        value = struct.unpack('<q', data)[0]

        # Currency fields are stored with 4 points of precision
        return Decimal(value) / 10000

    def parseB(self, field: Any, data: bytes) -> float | Any:
        """Binary memo field or double precision floating point number

        dBase uses B to represent a memo index (10 bytes), while
        Visual FoxPro uses it to store a double precision floating
        point number (8 bytes).
        """
        if self.dbversion in [0x30, 0x31, 0x32]:
            return struct.unpack('d', data)[0]
        else:
            return self.get_memo(self._parse_memo_index(data))

    def parseG(self, field: Any, data: bytes) -> Any:
        """OLE Object stored in memofile.

        The raw data is returned as a binary string."""
        return self.get_memo(self._parse_memo_index(data))

    def parseP(self, field: Any, data: bytes) -> Any:
        """Picture stored in memofile.

        The raw data is returned as a binary string."""
        return self.get_memo(self._parse_memo_index(data))

    # Autoincrement field ('+')
    parse2B = parseI

    # Timestamp field ('@')
    parse40 = parseT

    # Varchar field ('V') (Visual FoxPro)
    parseV = parseC
