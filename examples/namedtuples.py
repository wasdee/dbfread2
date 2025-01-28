"""
Return records as named tuples.

This saves a lot of memory.
"""
from collections import namedtuple

from dbfread22 import DBF

table = DBF('files/people.dbf', lowernames=True)

# Set record factory. This must be done after
# the table is opened because it needs the field
# names.
Record = namedtuple('Record', table.field_names)

def factory(lst):
    return Record(**dict(lst))

table.recfactory = factory

for record in table:
    print(record.name)
