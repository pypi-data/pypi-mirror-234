import filecmp
import shutil
import sqlite3
import os
import re
from pathlib import Path
from typing import Callable

import pytest

from dicomselect import Database, DICOMImageReader
from dicomselect.convert import LOG_FILENAME, Plan


@pytest.fixture(scope='session', autouse=True)
def output_expected_test_db():
    output_expected = Path('tests/output_expected')
    db_path = output_expected / 'test.db'
    db_path.parent.mkdir(exist_ok=True)
    db = Database(db_path)

    def custom_header_func(reader: DICOMImageReader):
        return {'custom_header': 'text', 'custom_header_int': 23}

    db.create('tests/input/ProstateX', max_workers=4, custom_header_func=custom_header_func)

    with sqlite3.connect(db_path) as conn:
        count = conn.execute('SELECT COUNT(*) FROM DATA;').fetchone()[0]
        assert count == 111, f'{db_path} does not contain 111 items!'

    return db


@pytest.fixture(scope='session')
def execute(output_expected_test_db: Database):
    output_expected = output_expected_test_db.path.parent
    output = Path('tests/output')
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    shutil.copytree(output_expected / 'convert', output / 'convert_existing')

    with output_expected_test_db as query:
        query_0000 = query.where('patient_id', '=', 'ProstateX-0000')
        query_0001 = query.where('patient_id', '=', 'ProstateX-0001')

    plan = output_expected_test_db.plan('{patient_id}/prostateX_{series_description}_{instance_creation_time}', query_0000, query_0001)
    plan.max_workers = 1
    plan.source_dir = Path('tests/input/ProstateX').absolute()
    plan.target_dir = (output / 'convert').absolute()

    def execute(dirname: str, postprocessfunc=None):
        plan.target_dir = (output / dirname).absolute()
        plan_str = plan.to_string()
        with open(output_expected / f'{dirname}.to_string.txt', encoding='utf-8', mode='r') as f:
            expected_str = f.read()
            assert len(expected_str[expected_str.find('├──'):]) == len(plan_str[plan_str.find('├──'):])

        plan.execute(postprocess_func=postprocessfunc)
        assert filecmp.dircmp(output_expected / dirname, output / dirname, ignore=[LOG_FILENAME]).diff_files == []

        output_log = output_expected / dirname / LOG_FILENAME
        assert not output_log.exists() ^ plan.path_log.exists()
        if output_log.exists():
            with open(plan.path_log, encoding='utf-8', mode='r') as a:
                with open(output_expected / dirname / LOG_FILENAME, encoding='utf-8', mode='r') as b:
                    assert len(a.read()) == len(b.read())  # asserting on content may fail due to random ordering

    return plan, execute


def test_convert(execute: (Plan, Callable)):
    plan, execute_func = execute
    execute_func('convert')


def test_convert_noop(execute):
    plan, execute_func = execute

    def postprocessfunc_noop(reader: DICOMImageReader):
        return reader.image

    execute_func('convert_noop', postprocessfunc_noop)


def test_convert_skip(execute):
    plan, execute_func = execute

    def postprocessfunc_skip(reader: DICOMImageReader):
        return False

    execute_func('convert_skip', postprocessfunc_skip)


def test_convert_split(execute):
    plan, execute_func = execute

    def postprocessfunc_split(reader: DICOMImageReader):
        return {'_a': reader.image, '_b': reader.image, '_c': reader.image}

    execute_func('convert_split', postprocessfunc_split)


def test_convert_existing(execute):
    plan, execute_func = execute

    with pytest.raises(AssertionError):
        execute_func('convert_existing')


def test_convert_missing(execute):
    plan, execute_func = execute
    plan.source_dir =  Path('tests/input/ProstateX-missing').absolute()

    with pytest.raises(RuntimeError):
        execute_func('convert_missing')


@pytest.mark.skipif(not os.path.exists('tests/input/temp') or len(os.listdir('tests/input/temp')) == 0,
                    reason='gitignored tests/input/temp directory is empty')
def test_convert_temp():
    try:
        db_path = Path('tests/output/test_temp.db')
        db = Database(db_path)
        if not db.path.exists():
            db_path.parent.mkdir(exist_ok=True)
            db.verify_dcm_filenames = False
            db.create('tests/input/temp', max_workers=4)
    except Exception as e:
        pytest.skip(f'test failed, run test_create.test_input_temp for details ({str(e)})')
    else:
        with db as query:
            query_0000 = query.where('patient_id', '=', '10016')
            query_0001 = query.where('patient_id', '=', '10051')

            if query_0000.count == 0 and query_0001.count == 0:
                pytest.skip('query contains no items')

        target_dir = Path('tests/output/convert_temp')
        if target_dir.exists():
            shutil.rmtree(target_dir)

        plan = db.plan('{patient_id}/temp_{series_description}_{sequence_name}', query_0000, query_0001)
        plan.max_workers = 1
        plan.target_dir = target_dir

        plan.to_string()
        plan.execute()

