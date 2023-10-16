import os
import sqlite3
from pathlib import Path

import pytest

from dicomselect import Database, DICOMImageReader


def test_input():
    db_path = Path('tests/output/test.db')
    db_path.parent.mkdir(exist_ok=True)
    db = Database(db_path)

    def custom_header_func(reader: DICOMImageReader):
        return {'custom_header': 'text', 'custom_header_int': 23}

    db.create('tests/input/ProstateX', max_workers=2, custom_header_func=custom_header_func)

    with sqlite3.connect(db_path) as conn:
        count = conn.execute('SELECT COUNT(*) FROM DATA;').fetchone()[0]
        assert count > 0, f'{db_path} contains no data ({count} > 0)'
        assert count > 100, f'{db_path} contains an unexpectedly low amount of data ({count} <= 100)'


def test_input_empty():
    db_path = Path('tests/output/test_empty.db')
    db_path.parent.mkdir(exist_ok=True)
    db = Database(db_path)

    with pytest.raises(sqlite3.DataError):
        db.create('tests/input/ProstateX-empty')


def test_input_flat():
    db_path = Path('tests/output/test_flat.db')
    db_path.parent.mkdir(exist_ok=True)
    db = Database(db_path)

    db.create('tests/input/ProstateX-flat', max_workers=1)

    with sqlite3.connect(db_path) as conn:
        count = conn.execute('SELECT COUNT(*) FROM DATA;').fetchone()[0]
        assert count > 0, f'{db_path} contains no data ({count} > 0)'
        assert count == 9, f'{db_path} contains an unexpected amount of data ({count} != 7)'


def test_input_duplicates():
    for flag, expected in [(1, 7), (2, 7), (3, 8)]:
        db_path = Path(f'tests/output/test_duplicates_{flag}.db')
        db_path.parent.mkdir(exist_ok=True)
        db = Database(db_path)
        db.prefer_mode = flag
        db.create('tests/input/ProstateX-duplicates', max_workers=1)

        with sqlite3.connect(db_path) as conn:
            count = conn.execute('SELECT COUNT(*) FROM DATA;').fetchone()[0]
            assert count > 0, f'{db_path} contains no data ({count} > 0)'
            assert count == expected, f'{db_path} contains an unexpected amount of data ({count} != {expected})'


@pytest.mark.skipif(not os.path.exists('tests/input/temp') or len(os.listdir('tests/input/temp')) == 0,
                    reason='gitignored tests/input/temp directory is empty')
def test_input_temp():
    db_path = Path('tests/output/test_temp.db')
    db_path.parent.mkdir(exist_ok=True)
    db = Database(db_path)
    db.verify_dcm_filenames = False

    db.create('tests/input/temp', max_workers=1)
