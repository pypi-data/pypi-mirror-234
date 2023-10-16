import binascii
import os
import re
import shutil
import sqlite3
import tempfile
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import PathLike
from pathlib import Path
from typing import Dict, Callable, Union, Optional, List

import pandas as pd
from tqdm import tqdm

from dicomselect.__version__ import __version__
from dicomselect.convert import Convert, Plan
from dicomselect.query import Query
from dicomselect.queryfactory import QueryFactory
from dicomselect.reader import DICOMImageReader
from dicomselect.logging import Logger

CustomHeaderFunction = Callable[[DICOMImageReader], Dict[str, Union[str, int, float]]]


class PreferMode:
    PreferZipFile = 1
    PreferDcmFile = 2


class Database(Logger):
    def __init__(self, db_path: PathLike):
        super().__init__()

        self._db_path = Path(db_path).absolute()
        if self._db_path.is_dir() or self._db_path.suffix != '.db':
            raise IsADirectoryError('Provide a file path with as extension, .db')
        self._conn: sqlite3.Connection = None
        self._query_factory: QueryFactory = None
        self._db_dir: Path = None
        self._is_warned_outdated_db = False

        self._prefer_mode = PreferMode.PreferZipFile
        self._verify_dcm_filenames = True

        self._headers: List[str] = None
        self._custom_header_func: CustomHeaderFunction = None
        self._custom_headers: Dict[str, type] = None
        self._additional_dicom_tags: List[str] = None

    @property
    def path(self) -> Path:
        return self._db_path

    @property
    def data_dir(self) -> Path:
        if not self._db_dir:
            try:
                with self:
                    self._db_dir = Path(self._conn.execute('SELECT datadir FROM meta').fetchone()[0])
            except Exception:
                raise sqlite3.DataError(f'No source directory found! Did you create a database at {self.path}?')
        return self._db_dir

    @property
    def version(self) -> str:
        if self.path.exists():
            cursor = sqlite3.connect(self.path, timeout=10)
            return cursor.execute('SELECT version FROM meta').fetchone()[0]
        return __version__

    @property
    def prefer_mode(self) -> int:
        return self._prefer_mode

    @prefer_mode.setter
    def prefer_mode(self, value: PreferMode):
        self._prefer_mode = value
        assert self._prefer_mode > 0, ValueError('Must have a filetype preference')

    @property
    def verify_dcm_filenames(self) -> bool:
        return self._verify_dcm_filenames

    @verify_dcm_filenames.setter
    def verify_dcm_filenames(self, value: bool):
        """
        Verify whether .dcm files in a directory are named logically (e.g. 01.dcm, 02.dcm, ..., 11.dcm with none missing)
        Set to False when .dcm filenames have no clear meaning.
        """
        self._verify_dcm_filenames = value

    def __enter__(self) -> Query:
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self) -> Query:
        with open(self.path, "rb") as f:
            file_header = binascii.hexlify(f.read(16)).decode("utf-8")

        # official sqlite3 file header
        if not file_header.startswith("53514c69746520666f726d6174203300"):
            raise sqlite3.DatabaseError(f'{self.path} does not appear to be a valid database')

        db_version = __version__.split('.')
        this_db_version = self.version.split('.')
        if db_version[0] != this_db_version[0]:
            raise RuntimeError(f'Error: this database ({this_db_version}) is outdated by a major revision {db_version}')
        if db_version[1] > this_db_version[1] and not self._is_warned_outdated_db:
            print(f'Warning: this database ({this_db_version}) is outdated by a minor revision {db_version}')
            self._is_warned_outdated_db = True

        self._conn = sqlite3.connect(self.path)
        self._query_factory = QueryFactory(self._conn)

        return self._query_factory.create_query(None)

    def close(self):
        self._conn.close()

    def plan(self, filepath_template: str, *queries: Query) -> Plan:
        """
        Prepare a conversion plan, which can convert the results of queries to MHA files.

        Parameters
        ----------
        filepath_template: PathLike
            Dictates the form of the directory and filename structure, omitting the suffix.
            Use braces along with column names to replace with that column value.
            Use forward slash to create a directory structure.
            (see Query.columns for a full list of available columns).
            A unique id will be appended at the end.

            Illegal characters will be replaced with '#'.
            Blank column values will be replaced with '(column_name)=blank'
        queries: Query
            The combined results of the query object will be converted to MHA.

        Returns
        -------
        A conversion plan.
        """
        with self as query:
            cols = query.columns
            requested_cols = [r.group(1) for r in re.finditer(r'{(.+?)}', filepath_template)]
            QueryFactory.check_if_exists('column', cols, *requested_cols)

            ids = set()
            for q in queries:
                ids = ids.union(q._ids)
            self._conn.execute('CREATE TEMPORARY TABLE convert_ids (id INTEGER)')
            self._conn.executemany('INSERT INTO convert_ids (id) VALUES (?)', [(i,) for i in ids])
            converts_fetched = self._conn.execute(
                f'SELECT dicomselect_uid, path, {", ".join(requested_cols)} FROM data JOIN convert_ids ON data.id = convert_ids.id').fetchall()
            converts = [Convert(fetched[0], fetched[1], filepath_template, requested_cols, fetched[2:]) for fetched in converts_fetched]

        if len(converts) == 0:
            raise ValueError('query contains no items!')

        return Plan(self.data_dir, converts)

    def create(self, data_dir: PathLike, max_workers: int = 4, custom_header_func: Optional[CustomHeaderFunction] = None, additional_dicom_tags: list[str] = None):
        """
        Build a database from DICOMs in data_dir.

        Parameters
        ----------
        data_dir: PathLike
            Directory containing .dcm data or dicom.zip data.
        max_workers
            Max number of workers for parallel execution of database creation.
        custom_header_func
            Create custom headers by returning a dict of [str, str | int | float] using the dicom reader.
            Note that using DICOMImageReader.image is a heavy operation and will significantly slow down database
            creation speed
        additional_dicom_tags
            See https://www.dicomlibrary.com/dicom/dicom-tags/, input any additional tags that are not included by default
            Each tag should be formatted as shown in the DICOM tag library, eg. '(0002,0000)'.
        """
        data_dir = Path(data_dir).absolute()

        self.init_logger(self.path.with_suffix('.log'))

        self._custom_header_func = custom_header_func
        self._additional_dicom_tags = additional_dicom_tags

        try:
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
                temp_db = Path(temp_dir) / 'temp.db'
                print(f'temp db is at {temp_db.as_posix()}')

                print(f'Scanning {data_dir}...')
                readers = self._scan_data_dir(data_dir, max_workers)
                readers_len = len(readers)
                if readers_len == 0:
                    raise sqlite3.DataError(f'No DICOM data found in {data_dir} ({self.errors} errors occurred)')

                with sqlite3.connect(temp_db, timeout=10) as cursor:
                    for i, reader in enumerate(readers, start=1):
                        try:
                            cursor.execute(f'CREATE TABLE data (id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT, {self._create_columns(reader)});')
                        except Exception as e:
                            if i < readers_len:
                                print(f'Error: {str(e)}. Retrying... ({i}/{readers_len})')
                            else:
                                raise e
                        else:
                            break

                print(f"Creating database of {readers_len} DICOMs from {data_dir}.")
                self._create_data_dir(data_dir, readers, temp_db, max_workers)

                with sqlite3.connect(temp_db, timeout=10) as cursor:
                    df_meta = pd.DataFrame({'datadir': str(data_dir), 'version': __version__}, index=[0])
                    df_meta.to_sql(name='meta', con=cursor, if_exists='replace')

                if self.path.exists():
                    os.remove(self.path)
                shutil.copy(temp_db, self.path)

                print(f"Database created at {self.path} with {self.errors} errors.")
        finally:
            if self.errors > 0:
                print(f'{self.errors} errors during database create: See {self.path_log} for details')

    def _collect_data(self, parent: Path, *filenames: str) -> List[DICOMImageReader]:
        """
        Prepare all data in data_dir as an uninitialized DICOMImageReader
        """
        readers = []
        files: Dict[str, list[str]] = {'.zip': [], '.dcm': None}
        for file in filenames:
            if file.endswith('.zip'):
                files['.zip'].append(file)
            if file.endswith('.dcm'):
                files['.dcm'] = file

        n = len({key for key in files.keys() if files[key]})
        if n == 1 or self.prefer_mode & PreferMode.PreferZipFile:
            for zipfile in files['.zip']:
                readers.append(DICOMImageReader(parent / zipfile, verify_dicom_filenames=self.verify_dcm_filenames, additional_tags=self._additional_dicom_tags))

        if files['.dcm'] and n == 1 or self.prefer_mode & PreferMode.PreferDcmFile:
            readers.append(DICOMImageReader(parent, verify_dicom_filenames=self.verify_dcm_filenames, additional_tags=self._additional_dicom_tags))

        return readers

    def _collect_data_walk(self, subdirectory: Path):
        readers = []
        for directory, _, filenames in os.walk(subdirectory, onerror=lambda err: self.log(traceback.format_exception(err))):
            readers.extend(self._collect_data(Path(directory), *filenames))
        return readers

    def _scan_data_dir(self, data_dir: Path, max_workers: int):
        chunk_size = max_workers
        readers = []
        for directory, subdirectories, filenames in os.walk(data_dir):
            directory = Path(directory)
            filenames_zip = [file for file in filenames if file.endswith('.zip')]

            if len(filenames_zip) > 0:  # zipfile multithreading mode
                if len([file for file in filenames if file.endswith('.dcm')]):
                    raise NotImplementedError('Found both .dcm and .zip in root directory')

                chunks = [filenames_zip[i:i + chunk_size] for i in range(0, len(filenames_zip), chunk_size)]
                with tqdm(total=len(filenames), desc='Scanning files') as pbar, ThreadPoolExecutor(
                        max_workers=max_workers) as pool:
                    futures = {pool.submit(self._collect_data, directory, *chunk): chunk for chunk in chunks}
                    for future in as_completed(futures.keys()):
                        try:
                            readers.extend(future.result())
                        except Exception as e:
                            self.log(e, name='file scan', filenames=futures[future])
                        pbar.update(chunk_size)
                        pbar.set_description(f'({self._errors} errors)')

            if len(subdirectories) > 1:  # subdirectory multithreading mode
                with tqdm(total=len(subdirectories), desc='Scanning directories') as pbar, ThreadPoolExecutor(
                        max_workers=max_workers) as pool:
                    futures = {pool.submit(self._collect_data_walk, directory / subdir): subdir for subdir in
                               subdirectories}
                    for future in as_completed(futures):
                        try:
                            readers.extend(future.result())
                        except Exception as e:
                            self.log(e, name='dir scan', subdir=futures[future])
                        pbar.update()
                        pbar.set_description(f'({self._errors} errors)')
                break

            elif len(subdirectories) == 0:  # single file, simply collect singlethreaded
                readers.extend(self._collect_data(directory, *filenames))

        return readers

    def _create_columns(self, reader: DICOMImageReader):
        """
        Obtain columns from any (uninitialized) DICOMImageReader
        """
        dicom_columns, custom_columns = [], []

        # confirm these do not break
        dicom_metadata = reader.metadata | {'path': ''}
        custom_metadata = self._custom_header_func_runner(reader, dicom_metadata)

        # populate SQL columns
        self._custom_headers = {}
        dicom_columns = [f'{name} {dtype}' for name, dtype in reader.column_info().items()]
        for key, value in custom_metadata.items():  # split custom values into SQL datatypes
            for T, dtype in [(str, 'TEXT'), (int, 'INTEGER'), (float, 'REAL')]:
                if isinstance(value, T):
                    self._custom_headers[key] = T  # apply contract that this key must be of type T
                    custom_columns.append(f'{key} {dtype}')  # SQL column header
                    break

        if dicom_metadata is None or len(dicom_columns) == 0:
            raise sqlite3.DataError('No DICOM data found')

        self._headers = set(dicom_metadata.keys()).union(set(custom_metadata.keys()))
        return ', '.join(sorted(dicom_columns + custom_columns))

    def _create_data_dir(self, data_dir: Path, readers: List[DICOMImageReader], temp_db: Path, max_workers: int):
        existing_errors_len = self.errors
        chunk_size = max_workers
        chunks = [readers[i:i + chunk_size] for i in range(0, len(readers), chunk_size)]
        with tqdm(total=len(readers)) as pbar, ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(self._thread_execute, temp_db, data_dir, chunk): chunk for chunk in chunks}
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    self.log(e, name='create', DICOMImageReaders=futures[future])
                pbar.update(chunk_size)
                pbar.set_description(f'({self.errors - existing_errors_len} errors)')

    def _custom_header_func_runner(self, reader: DICOMImageReader, existing_metadata: dict):
        if self._custom_header_func:
            custom_metadata = self._custom_header_func(reader)
            for key, value in custom_metadata.items():
                assert key not in existing_metadata, KeyError(f"'{key}' already exists in metadata")
                assert isinstance(key, str), KeyError("Custom headers must be of type 'str'")

                if self._custom_headers:
                    # during database creation, we check if the header maintains expected type as per the prior example
                    expected_type = self._custom_headers[key]
                    assert isinstance(value, expected_type), ValueError(f"Value in custom header '{key}' must be of type '{expected_type.__name__}'")
                else:
                    assert isinstance(value, (str, int, float)), \
                        ValueError(f"Values in custom header '{key}' must be one of types 'str', 'int', 'float'")
            return custom_metadata
        return {}

    def _extract_metadata(self, data_dir: Path, reader: DICOMImageReader):
        metadata = dict()
        try:
            metadata = reader.metadata.copy()
            metadata["path"] = str(reader.path.relative_to(data_dir))
            metadata |= self._custom_header_func_runner(reader, metadata)
            reader.clear()
        except BaseException as e:
            self.log(e)
        if metadata:
            return metadata

    def _thread_execute(self, db: Path, data_dir: Path, readers: List[DICOMImageReader]):
        with sqlite3.connect(db, timeout=10, check_same_thread=False) as conn:
            metadata = []
            for reader in readers:
                if md := self._extract_metadata(data_dir, reader):
                    metadata.append({key: value for key, value in md.items() if key in self._headers})
            df_rows = pd.DataFrame.from_dict(metadata, orient='columns')
            df_rows.to_sql(name='data', con=conn, if_exists='append', index=False)
