# Field Types

## Supported Field Types

| Type | Field Type    | Python Type                                         |
| ---- | ------------- | --------------------------------------------------- |
| +    | autoincrement | `int`                                               |
| @    | time          | `datetime.datetime`                                 |
| 0    | flags         | `bytes` (byte string)                               |
| B    | double/memo   | `float` (Visual FoxPro) or `bytes` (other versions) |
| C    | text          | `str` (unicode string)                              |
| D    | date          | `datetime.date` or `None`                           |
| F    | float         | `float`                                             |
| G    | OLE object    | `bytes` (byte string)                               |
| I    | integer       | `int`                                               |
| L    | logical       | `bool` (`True`, `False`) or `None`                  |
| M    | memo          | `str` (memo), `bytes` (picture/object) or `None`    |
| N    | numeric       | `int`, `float` or `None`                            |
| O    | double        | `float` (floats are doubles in Python)              |
| P    | picture       | `bytes` (byte string)                               |
| T    | time          | `datetime.datetime`                                 |
| V    | varchar       | `str` (unicode string)                              |
| Y    | currency      | `decimal.Decimal`                                   |

!!! note "Text Field Length"
Text values ('C') can be up to 65535 bytes long. While DBF was originally limited to 255 bytes, some vendors reuse the `decimal_count` field to get another byte for field length.

!!! info "Type B Field"
The 'B' field type serves two purposes: 1. Store double precision (64 bit) floats in Visual FoxPro databases 2. Store binary memos in other versions

    dbfread2 examines the database version to parse and return the correct data type.

!!! warning "Type 0 Field"
The '0' field type is used for '\_NullFlags' in Visual FoxPro. It was previously interpreted as an integer, but from version 2.0.1 onward it is returned as a byte string.

!!! note "Type V Field"
The 'V' field is an alternative character field used by Visual FoxPro. The binary version is not yet supported. See [Microsoft Documentation](https://msdn.microsoft.com/en-us/library/st4a0s68%28VS.80%29.aspx) for more details.

## Adding Custom Field Types

You can add new field types by subclassing `FieldParser`:

```python
from dbfread2 import DBF, FieldParser

class MyFieldParser(FieldParser):
    def parseC(self, field, data):
        """Custom parser for text fields"""
        return data.rstrip(b' 0').decode(self.encoding)

table = DBF('data.dbf', parserclass=MyFieldParser)
```

### FieldParser Attributes

The `FieldParser` class provides these attributes:

- `self.table`: Reference to the `DBF` object (access headers, dbversion, etc.)
- `self.encoding`: Character encoding (shortcut for `self.table.encoding`)
- `self.char_decode_errors`: Error handling scheme for decoding
- `self.dbversion`: Database version as integer
- `self.get_memo(index)`: Get memo from memo file using field data index
- `self.decode_text(text)`: Decode text using correct encoding and error handling

### Memo Types

For Visual FoxPro (`.FPT`) files, `get_memo()` returns specialized types:

```
bytes
└── VFPMemo
    ├── TextMemo
    └── BinaryMemo
        ├── PictureMemo
        └── ObjectMemo
```

All types are subclasses of `bytes` to maintain compatibility while annotating memo types.

## Special Characters in Field Type Names

For field types with special characters (like '+'), use the ASCII value in hexadecimal:

```python
# For field type '+', use:
def parse2B(self, field, data):  # 2B is hex for '+'
    pass

# To get the method name:
method_name = 'parse' + format(ord('+'), 'x').upper()  # Returns 'parse2B'
```

## Handling Invalid Values

Instead of raising `ValueError` for invalid data, you can return raw data using `InvalidValue`:

```python
from dbfread2 import DBF, FieldParser, InvalidValue

class SafeParser(FieldParser):
    def parse(self, field, data):
        try:
            return super().parse(field, data)
        except ValueError:
            return InvalidValue(data)

table = DBF('data.dbf', parserclass=SafeParser)
for record in table:
    for name, value in record.items():
        if isinstance(value, InvalidValue):
            print(f'Invalid value in {name}: {value!r}')
```
