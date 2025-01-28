"""
Return records as objects with fields as attributes.
"""
from dbfread2 import DBF


class Record:
    def __init__(self, items):
        for name, value in items:
            setattr(self, name, value)

for record in DBF('files/people.dbf', record_factory=Record, lowercase_names=True):
    print(record.name, 'was born on', record.birthdate)
