# Introduction

This is a short introduction to the API. The example files used in this guide can be found in the `examples/files/` directory.

## Opening a DBF File

```python
from dbfread2 import DBF
table = DBF('people.dbf')
```

You can iterate over records:

```python
for record in table:
    print(record)
# {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)}
# {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}
```

Records will be returned in the order they appear in the file.

You can count records:

```python
len(table)  # Returns: 2
```

Deleted records are available in `deleted`:

```python
for record in table.deleted:
    print(record)
# {'NAME': 'Deleted Guy', 'BIRTHDATE': datetime.date(1979, 12, 22)}

len(table.deleted)  # Returns: 1
```

You can also use the `with` statement:

```python
with DBF('people.dbf') as table:
    ...
```

!!! note
The DBF object doesn't keep any files open, so the `with` statement is provided merely as a convenience.

## Streaming vs Loading Records

By default, records are streamed directly from disk, meaning only one record is in memory at a time.

If you have enough memory, you can load all records into a list by passing `load=True`. This allows for random access:

```python
table = DBF('people.dbf', load=True)
print(table.records[1]['NAME'])  # Returns: 'Bob'
print(table.records[0]['NAME'])  # Returns: 'Alice'
```

Deleted records are also loaded into a list in `table.deleted`.

Alternatively, you can:

1. Load records later by calling `table.load()`
2. Get a simple list of records with `records = list(DBF('people.dbf'))`
3. Unload records with `table.unload()`

!!! note
If the table is not loaded, the `records` and `deleted` attributes return `RecordIterator` objects.

## Character Encodings

All text fields and memos (except binary ones) are returned as unicode strings.

dbfread2 will:

1. Try to detect the character encoding (code page) from the `language_driver` byte
2. Fallback to ASCII if detection fails
3. Allow override with `encoding='my-encoding'`

You can handle decoding errors with the `char_decode_errors` option, which is passed to `bytes.decode()`.

## Memo Files

For files with memo fields, dbfread2 will look for the corresponding memo file:

- `buildings.fpt` (Visual FoxPro)
- `buildings.dbt` (other databases)

### Case Sensitivity

By default, dbfread2 ignores case in file names to handle mixed-case files in case-sensitive systems. You can disable this with `ignorecase=False`.

### Missing Memo Files

If a memo file is missing:

1. A `MissingMemoFile` exception is raised by default
2. Pass `ignore_missing_memofile=True` to continue with memo fields as `None`

### Memo File Support

- Full support for Visual FoxPro (`.FPT`)
- Full support for dBase III (`.DBT`)
- Partial support for dBase IV (`.DBT`) - only with default 512-byte blocks

## Record Factories

You can customize record format with the `recfactory` argument:

```python
class Record:
    def __init__(self, items):
        for (name, value) in items:
            setattr(self, name, value)

# Use custom record class
for record in DBF('people.dbf', recfactory=Record, lowernames=True):
    print(record.name, record.birthdate)
```

Pass `recfactory=None` to get the original `(name, value)` list.

## Custom Field Types

You can add custom field types by subclassing `FieldParser`:

```python
from dbfread2 import DBF, FieldParser

class ReverseTextParser(FieldParser):
    def parseC(self, field, data):
        # Return strings reversed
        return data.rstrip(' 0').decode()[::-1]

for record in DBF('people.dbf', parserclass=ReverseTextParser):
    print(record['NAME'])
```

### Handling Invalid Values

```python
from dbfread2 import DBF, FieldParser, InvalidValue

class SafeParser(FieldParser):
    def parse(self, field, data):
        try:
            return FieldParser.parse(self, field, data)
        except ValueError:
            return InvalidValue(data)

table = DBF('invalid_value.dbf', parserclass=SafeParser)
for i, record in enumerate(table):
    for name, value in record.items():
        if isinstance(value, InvalidValue):
            print(f'records[{i}][{name!r}] == {value!r}')
```
