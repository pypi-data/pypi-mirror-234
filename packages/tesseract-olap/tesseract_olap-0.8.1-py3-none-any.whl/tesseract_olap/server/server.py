import logging
from pathlib import Path
from typing import Union, overload

from tesseract_olap.backend import Backend
from tesseract_olap.query import (DataQuery, DataRequest, DataResult,
                                  MembersQuery, MembersRequest, MembersResult)
from tesseract_olap.query.exceptions import InvalidQuery, NotAuthorized
from tesseract_olap.schema import Schema, SchemaTraverser

from .exceptions import UnknownBackendError
from .schema import setup_schema

logger = logging.getLogger("tesseract_olap.server")


class OlapServer:
    """Main server class.

    This object manages the connection with the backend database and the schema
    instance containing the database references, to enable make queries against
    them.
    """
    schema: "SchemaTraverser"
    backend: "Backend"

    def __init__(self,
                 backend: Union[str, "Backend"],
                 schema: Union[str, "Path", "Schema"]):
        self.backend = (
            backend
            if isinstance(backend, Backend) else
            _setup_backend(backend)
        )

        self.schema = SchemaTraverser(
            schema
            if isinstance(schema, Schema) else
            setup_schema(schema)
        )

    @property
    def raw_schema(self):
        """Retrieves the raw Schema instance used by this server."""
        return self.schema.schema

    async def connect(self):
        """Initializes the connection to the backend server."""
        self.schema.validate()
        await self.backend.connect()
        await self.backend.validate_schema(self.schema)

    async def disconnect(self):
        """Terminates cleanly the currently active connections."""
        self.backend.close()
        await self.backend.wait_closed()

    async def ping(self) -> bool:
        """Performs a ping call to the backend server.
        A succesful call should make this function return :bool:`True`.
        """
        try:
            return await self.backend.ping()
        except IndexError:
            return False

    @overload
    async def execute(self, request: DataRequest, **kwargs) -> DataResult:
        ...
    @overload
    async def execute(self, request: MembersRequest, **kwargs) -> MembersResult:
        ...
    async def execute(
        self,
        request: Union[DataRequest, MembersRequest],
        **kwargs
    ) -> Union[DataResult, MembersResult]:
        """
        If the request is an instance of :class:`DataRequest`, gets the aggregated
        data from the backend and wraps it in a :class:`DataResult` object.
        If the request is an instance of :class:`MembersRequest`, gets the list
        of categories associated to the requested level and wraps the result in
        a :class:`MembersResult` object.
        """

        if not self.schema.is_authorized(request):
            raise NotAuthorized()

        # The `first` pattern forces the driver to raise any errors in the body
        # of this function, so this can be safely wrapped in a try/except block.

        if isinstance(request, MembersRequest):
            query = MembersQuery.from_request(self.schema, request)
            data = self.backend.execute(query, **kwargs)
            try:
                first = await data.__anext__()
            except StopAsyncIteration:
                first = None
            return MembersResult(first, data, request)

        if isinstance(request, DataRequest):
            query = DataQuery.from_request(self.schema, request)
            data = self.backend.execute(query, **kwargs)
            try:
                first = await data.__anext__()
            except StopAsyncIteration:
                first = None
            sources = query.get_sources()
            return DataResult(first, data, sources, request)

        raise InvalidQuery(
            "OlapServer only accepts instances of DataRequest or MembersRequest"
        )


def _setup_backend(connection: str):
    """Generates a new instance of a backend bundled in this package, or raises
    an error if no one is compatible, with a provided connection string.
    """
    if connection.startswith("clickhouse:") or connection.startswith("clickhouses:"):
        from tesseract_olap.backend.clickhouse import ClickhouseBackend
        return ClickhouseBackend(connection)

    raise UnknownBackendError(connection)
