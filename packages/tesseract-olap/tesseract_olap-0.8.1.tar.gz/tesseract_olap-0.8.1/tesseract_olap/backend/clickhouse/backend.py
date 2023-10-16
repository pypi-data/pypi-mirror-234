import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, Optional, Type, TypeVar, Union

import asynch
from asynch.cursors import Cursor, DictCursor
from asynch.errors import ClickHouseException
from asynch.proto.result import IterQueryResult

from tesseract_olap.backend import Backend
from tesseract_olap.backend.exceptions import (UnexpectedResponseError,
                                               UpstreamInternalError)
from tesseract_olap.common import AnyDict
from tesseract_olap.query import DataQuery, MembersQuery
from tesseract_olap.query.exceptions import InvalidQuery
from tesseract_olap.schema import CubeTraverser, InlineTable, SchemaTraverser

from .dialect import ClickhouseDataType
from .sqlbuild import dataquery_sql, membersquery_sql

logger = logging.getLogger("tesseract_olap.backend.clickhouse")

CursorType = TypeVar("CursorType", bound=Cursor)


class ClickhouseBackend(Backend):
    """Clickhouse Backend class

    This is the main implementation for Clickhouse of the core :class:`Backend`
    class.

    Must be initialized with a connection string with the parameters for the
    Clickhouse database. Then must be connected before used to execute queries,
    and must be closed after finishing use.
    """

    connection_string: str

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string

    def __repr__(self) -> str:
        return f"ClickhouseBackend('{self.connection_string}')"

    async def connect(self, **kwargs):
        pass

    @asynccontextmanager
    async def acquire(
        self, curcls: Type[CursorType] = Cursor
    ) -> AsyncGenerator[CursorType, None]:
        conn = await asynch.connect(dsn=self.connection_string)
        try:
            async with conn.cursor(cursor=curcls) as cursor:
                yield cursor  # type: ignore
        except ClickHouseException as exc:
            tb = exc.__traceback__
            raise UpstreamInternalError(str(exc)).with_traceback(tb)
        except Exception as exc:
            tb = exc.__traceback__
            raise UnexpectedResponseError(str(exc)).with_traceback(tb)
        finally:
            await conn.close()

    def close(self):
        pass

    async def wait_closed(self):
        pass

    async def execute(
        self, query: Union["DataQuery", "MembersQuery"], **kwargs
    ) -> AsyncGenerator[AnyDict, None]:
        """
        Performs a query for data against the database server.

        Processes the requests in a :class:`DataQuery` or :class:`MembersQuery`
        instance, sends the query to the database, and returns an `AsyncIterator`
        to access the rows.
        Each iteration yields a tuple of the same length, where the first tuple
        defines the column names, and the subsequents are rows with the data in
        the same order as each column.
        """
        logger.debug("Execute query", extra={"query": query})

        ext_tables: List[InlineTable] = []

        if isinstance(query, MembersQuery):
            sql_builder, sql_params, tables = membersquery_sql(query)
            ext_tables.extend(tables)
        elif isinstance(query, DataQuery):
            sql_builder, sql_params, tables = dataquery_sql(query)
            ext_tables.extend(tables)
        else:
            raise InvalidQuery(
                "ClickhouseBackend only supports DataQuery and MembersQuery instances"
            )

        async with self.acquire(CustomCursor) as cursor:
            for table in ext_tables:
                structure = zip(table.headers, (
                    ClickhouseDataType.from_membertype(item).value
                    for item in table.types
                ))
                cursor.set_external_table(table.name, list(structure), table.rows)

            sql = sql_builder.get_sql()
            await cursor.execute(query=sql, args=sql_params)
            # AsyncGenerator must be fully consumed before returning,
            # otherwise async context closes connection prematurely
            async for row in cursor.iterall():
                yield row

    async def ping(self) -> bool:
        """Checks if the current connection is working correctly."""
        async with self.acquire() as cursor:
            await cursor.execute("SELECT 1")
            result = await cursor.fetchone()
            return result == (1,)

    async def validate_schema(self, schema: "SchemaTraverser"):
        """Checks all the tables and columns referenced in the schema exist in
        the backend.
        """
        # logger.debug("Schema %s", schema)
        for cube in schema.cube_map.values():
            await self._validate_cube(cube)

    async def _validate_cube(self, cube: "CubeTraverser"):
        """"""
        if isinstance(cube.table, InlineTable):
            return None

        logger.debug("Validating schema for Cube %s", cube.name)

        # Validate fact table
        async with self.acquire(DictCursor) as cursor:
            table_name = f"{cube.table.name}".split(" ")[0]
            await cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
            result = await cursor.fetchone()

        for item in cube.measures:
            assert item.key_column in result
        for item in cube.dimensions:
            assert item.foreign_key in result

        # TODO: Validate dimension tables


class CustomCursor(Cursor):
    def __init__(self, connection=None, echo=False):
        super().__init__(connection, echo)
        self.set_stream_results(True, 5000)

    async def iterall(self) -> AsyncGenerator[AnyDict, None]:
        self._check_query_started()

        columns = self._columns
        if not isinstance(columns, (tuple, list)) or len(columns) == 0:
            raise UpstreamInternalError("Clickhouse did not return information about columns.")

        if isinstance(self._rows, IterQueryResult):
            async for row in self._rows:
                yield dict(zip(columns, row))

        else:
            raise ValueError("Streaming result not enabled")

    async def execute(self, query: str, args: Optional[dict]=None, context=None):
        self._check_cursor_closed()
        self._check_query_executing()
        self._begin_query()

        execute, kwargs = self._prepare(context)

        del kwargs["settings"]["max_block_size"]

        response = await execute(query, args=args, with_column_types=True, **kwargs)

        await self._process_response(response)
        self._end_query()

        return self._rowcount
