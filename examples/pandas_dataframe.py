"""
Load content of a DBF file into a Pandas data frame.

The iter() is required because Pandas doesn't detect that the DBF
object is iterable.
"""
from pandas import DataFrame

from dbfread2 import DBF

dbf = DBF('files/people.dbf')
frame = DataFrame(iter(dbf))

print(frame)
