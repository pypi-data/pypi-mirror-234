import sqlite3
from typing import Tuple, Optional, Iterable, Dict, List

import rapidfuzz


class QueryFactory:
    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection
        self._cursor = connection.cursor()
        column_info = self.execute('PRAGMA TABLE_INFO(data)').fetchall()
        self.columns: Tuple[str] = tuple([c[1] for c in column_info if c[1] != 'id'])
        self.temp_tables: Dict[str, Tuple[List[int], int]] = dict()
        self._update_temp_tables('data')
        self._count = -1

    def execute(self, sql: str) -> sqlite3.Cursor:
        return self._cursor.execute(sql)

    def create_query(self, parent: Optional[str]):
        from dicomselect.query import Query
        return Query(self, parent)

    def _update_temp_tables(self, new_temp_table: str):
        ids = self.select_ids(new_temp_table)
        self.temp_tables[new_temp_table] = (ids, len(ids))
        self.temp_tables = dict(sorted(self.temp_tables.items(), key=lambda x: x[1][1]))

    def create_query_from_sql(self, sql: str, parent_temp_table: str):
        new_temp_table = __package__ + str(len(self.temp_tables))
        if parent_temp_table:
            self.execute(
                f'CREATE TEMP TABLE {new_temp_table} AS SELECT id FROM {parent_temp_table} WHERE id IN (SELECT id FROM data {sql});')
        else:
            self.execute(f'CREATE TEMP TABLE {new_temp_table} AS SELECT id FROM data {sql};')

        self._update_temp_tables(new_temp_table)
        return self.create_query(new_temp_table)

    def create_query_from_set_operation(self, temp_table_a: str, temp_table_b: str, operation: str):
        self.check_if_exists('query', self.temp_tables.keys(), temp_table_b)
        temp_tables = [key for key in self.temp_tables.keys() if key == temp_table_a or key == temp_table_b]

        new_temp_table = __package__ + str(len(self.temp_tables))
        self.execute(f'CREATE TEMP TABLE {new_temp_table} AS SELECT id FROM {temp_tables[0]} {operation} SELECT id FROM {temp_tables[1]};')

        self._update_temp_tables(new_temp_table)
        return self.create_query(new_temp_table)

    def select_ids(self, table: str):
        return [i[0] for i in self.execute(f'SELECT id FROM {table};').fetchall()]

    @staticmethod
    def check_if_exists(item_type: str, possible_items: Iterable, *items):
        for item in items:
            if item is not None and item not in possible_items:
                suggest = rapidfuzz.process.extractOne(item, possible_items, score_cutoff=25)
                suggest = f', did you mean {suggest[0]}?' if suggest else ''
                raise ValueError(f'{item_type} "{item}" does not exist{suggest}')
