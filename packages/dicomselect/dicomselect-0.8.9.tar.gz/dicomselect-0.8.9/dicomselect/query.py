from typing import TYPE_CHECKING, Dict, List, Tuple, Union

if TYPE_CHECKING:
    from dicomselect.queryfactory import QueryFactory

from dicomselect.info import Info


class Query:
    def __init__(self, factory: 'QueryFactory', name: str):
        self._factory = factory
        self._name = name or 'data'
        ids = factory.temp_tables[self._name]
        self._ids = ids[0]
        self._count = ids[1]

    @property
    def is_base(self) -> bool:
        return not bool(self._name)

    @property
    def count(self) -> int:
        return self._count

    @property
    def columns(self):
        """
        Return a tuple containing the names of all the columns in the database.

        Returns
        -------
        Tuple
            A tuple of column names.
        """
        return self._factory.columns

    def info(self):
        """
        Returns an Info object which can print out the current query selection
        """
        rows: List[tuple] = self._factory.execute(
            f'SELECT DISTINCT * FROM data WHERE id IN (SELECT id FROM {self._name})').fetchall()
        cols: Dict[Dict[str, int]] = dict()
        for i, c in enumerate(self.columns, 1):
            cols[c] = {}
            for r in rows:
                value = r[i]
                cols[c][value] = cols[c].get(value, 0) + 1
        return Info(self, rows, cols)

    def distinct_values(self, column: str) -> List[str]:
        """
        Retrieve distinct values from a specified column.

        Parameters
        ----------
        column : str
            The name of the column to retrieve distinct values from.
        """
        if not self.is_base:
            distinct: List[Tuple[str]] = self._factory.execute(
                f'SELECT DISTINCT {column} FROM data WHERE id IN (SELECT id FROM {self._name})'
            ).fetchall()
        else:
            distinct: List[Tuple[str]] = self._factory.execute(f'SELECT DISTINCT ({column}) FROM data').fetchall()
        return [d[0] for d in distinct]

    def where_raw(self, sql: str) -> 'Query':
        """
        Create a query based on a raw SQL query.

        Parameters
        ----------
        sql : str
            SQL query. "... WHERE" is prefixed.

        Raises
        ------
        ValueError
            Invalid SQL.
        """
        return self._factory.create_query_from_sql('WHERE ' + sql, self._name if not self.is_base else '')

    def where(self, column: str, operator: str, values: Union[List[str], str], invert: bool = False) -> 'Query':
        """
        Filter the dataset based on the given column, operator, and values. The result can be combined with other queries
        using the union(), difference(), and intersect() methods.

        Parameters
        ----------
        name : str or list of str
            Query identifier. Used to operate with union(), difference(), and intersect() methods.
        column : str
            Name of the column to query. The name is case-sensitive. The columns property can be used to obtain a list
            of all available columns.
        operator : str
            Valid operators include '=', '<>', '!=', '>', '>=', '<', '<=', 'like', 'between', and 'in'.
        *values : str
            Values to query. Providing more values than expected will create OR chains, eg. (column='a') OR (column='b'),
            where appropriate
        invert: bool, optional
            Invert the query, by prefixing the query with a NOT.
        """
        loc = locals()
        self._factory.check_if_exists('column', self.columns, loc['column'])

        values = values if isinstance(values, list) else [values]
        values = [f"'{v}'" for v in values]
        len_values = len(values)
        valid_operators = '=', '<>', '!=', '>', '>=', '<', '<=', 'LIKE', 'BETWEEN', 'IN'
        operator = operator.upper()
        invert = 'NOT' if invert else ''
        assert len_values > 0, ValueError('expected values, got 0')

        if operator not in valid_operators:
            raise ValueError(f'{operator} is an invalid operator, valid operators are {valid_operators}')

        if operator == 'BETWEEN':
            if len(values) % 2 != 0:
                raise ValueError(f'expected an even number of values, got {len(values)}: {values}')
            values = [f'({column} BETWEEN {values[i]} AND {values[i + 1]})' for i in range(0, len(values), 2)]
        elif operator == 'IN':
            values = [f'{column} IN (' + ', '.join(values) + ')']
        else:
            values = [f'({column} {operator} {v})' for v in values]

        values = ' OR '.join(values)
        sql = f'WHERE {invert} ({values})'
        return self._factory.create_query_from_sql(sql, self._name if not self.is_base else '')

    def intersect(self, where: 'Query') -> 'Query':
        """
        Create a new view by intersecting the results of the specified queries.

        Parameters
        ----------
        where : Query
            The query to intersect. Leave empty to intersect using the last two queries.

        Raises
        ------
        ValueError
            If any of the specified queries do not exist.
        """
        return self._factory.create_query_from_set_operation(self._name, where._name, 'INTERSECT')

    def union(self, where: 'Query') -> 'Query':
        """
        Create a new query by taking the union of the results of the specified queries.

        Parameters
        ----------
        where : Query
            The query to union. Leave empty to union using the last two queries.

        Raises
        ------
        ValueError
            If any of the specified queries do not exist.
        """
        return self._factory.create_query_from_set_operation(self._name, where._name, 'UNION')

    def difference(self, where: 'Query') -> 'Query':
        """
        Create a new query by taking the difference of the results of the specified queries.

        Parameters
        ----------
        where : Query
            The query to subtract. Leave empty to subtract using the last two queries.

        Raises
        ------
        ValueError
            If any of the specified queries do not exist.
        """
        return self._factory.create_query_from_set_operation(self._name, where._name, 'EXCEPT')

    def __str__(self) -> str:
        return str(self.info().exclude(recommended=True, exclude_none_distinct=True))
