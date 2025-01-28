from pytest import raises

from dbfread2 import DBF, MissingMemoFileError


def test_missing_memofile():
    with raises(MissingMemoFileError):
        DBF('tests/cases/no_memofile.dbf')

    # This should succeed.
    table = DBF('tests/cases/no_memofile.dbf', ignore_missing_memo=True)

    # Memo fields should be returned as None.
    record = next(iter(table))
    assert record['MEMO'] is None
