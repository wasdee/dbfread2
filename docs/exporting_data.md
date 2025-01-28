# Exporting Data

dbfread2 makes it easy to export data to various formats and systems.

## CSV Export

Using Python's built-in `csv` module:

```python
import csv
from dbfread2 import DBF

table = DBF('people.dbf')

with open('people.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(table.field_names)  # Write headers
    for record in table:
        writer.writerow([record[field] for field in table.field_names])
```

Output:

```csv
NAME,BIRTHDATE
Alice,1987-03-01
Bob,1980-11-12
```

## Pandas DataFrames

```python
import pandas as pd
from dbfread2 import DBF

table = DBF('people.dbf')
df = pd.DataFrame(iter(table))  # iter() is required
print(df)
```

Output:

```
        BIRTHDATE   NAME
0  1987-03-01  Alice
1  1980-11-12    Bob
```

!!! note "Memory Usage"
Pandas will load all records into memory when creating the DataFrame.
This is a limitation of pandas and cannot be avoided.

## SQL with dataset

Using [dataset](https://dataset.readthedocs.io/) for easy database operations:

```python
import dataset
from dbfread2 import DBF

# Open database connection
db = dataset.connect('sqlite:///example.db')

# Read DBF and insert into database
table = DBF('people.dbf')
db['people'].insert_many(iter(table))
```

This will:

1. Create the table schema automatically
2. Insert all records from the DBF file

## Command Line Export to SQLite

dbfread2 includes a command-line tool for SQLite export:

```bash
# Export to SQLite file
dbfread2-sqlite -o example.sqlite table1.dbf table2.dbf

# Print SQL to stdout
dbfread2-sqlite table1.dbf table2.dbf

# Handle encoding issues
dbfread2-sqlite --encoding=latin1 -o example.sqlite table1.dbf
```

Features:

- Creates one table per DBF file
- Automatic schema creation
- Configurable character encoding
- Optional SQL output to stdout
