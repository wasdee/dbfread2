"""
Tests reading from database.
"""
import datetime

from pytest import fixture

from dbfread2 import DBF


@fixture
def table():
    return DBF('tests/cases/memotest.dbf')

@fixture
def loaded_table():
    return DBF('tests/cases/memotest.dbf', preload=True)

# This relies on people.dbf having this exact content.
records = [{'NAME': 'Alice',
            'BIRTHDATE': datetime.date(1987, 3, 1),
            'MEMO': 'Alice memo'},
           {'NAME': 'Bob',
            'BIRTHDATE': datetime.date(1980, 11, 12),
            'MEMO': 'Bob memo'}]
deleted_records = [{'NAME': 'Deleted Guy',
                    'BIRTHDATE': datetime.date(1979, 12, 22),
                    'MEMO': 'Deleted Guy memo'}]

def test_len(table, loaded_table):
    assert len(table) == 2
    assert len(table.deleted) == 1

    assert len(loaded_table) == 2
    assert len(loaded_table.deleted) == 1


def test_list(table, loaded_table):
    assert list(table) == records
    assert list(table.deleted) == deleted_records

    assert list(loaded_table) == records
    assert list(loaded_table.deleted) == deleted_records

    # This should not return old style table which was a subclass of list.
    assert not isinstance(table, list)
