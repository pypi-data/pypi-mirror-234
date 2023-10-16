"""Backend model definitions module.

This module contains abstract definitions for the interfaces of the Backend
class. Tesseract is compatible with any kind of data source as long as there's a
backend class that adapts the Query and the Results to the defined interface.
"""

import abc
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, AsyncGenerator, Dict, Optional, Union

from tesseract_olap.common import AnyDict, shorthash

if TYPE_CHECKING:
    from tesseract_olap.query import DataQuery, MembersQuery
    from tesseract_olap.schema import SchemaTraverser


class Backend(abc.ABC):
    """Base class for database backends compatible with Tesseract."""

    @abc.abstractmethod
    async def connect(self, **kwargs):
        """Establishes the connection to the backend server.

        This operation must be done before running any other data method, and
        must be separate from the creation of a :class:`Backend` instance.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def close(self):
        """Performs the needed operations to safely close the connection with
        the backend server.

        This method is synchronous for compatibility with the signature of other
        `close()` calls, but since closing operations are asynchronous, the
        closing procedure must be combined with the `wait_closed()` method, and
        can only be considered finished when it succeeds.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def wait_closed(self):
        """Creates a Coroutine which waits until the whole closing procedure
        finishes to completion."""
        raise NotImplementedError()

    @abc.abstractmethod
    def execute(
        self,
        query: Union["DataQuery", "MembersQuery"],
        **kwargs
    ) -> AsyncGenerator[AnyDict, None]:
        """Processes the requests in a :class:`DataQuery` or :class:`MembersQuery`
        instance, sends the query to the database, and returns an `AsyncIterator`
        to access the rows.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def ping(self) -> bool:
        """Performs a ping call to the backend server.
        If the call is successful, this function should return :bool:`True`.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def validate_schema(self, schema: "SchemaTraverser") -> None:
        """Ensures all columns defined in the schema are present in the backend.
        Should raise if it find any problem, otherwise should return `None`.
        """
        raise NotImplementedError()


@dataclass
class ParamManager:
    """Keeps track of the SQL named parameters and their values, to combine them
    through all the functions where they're defined, and output them at the
    final generation step.
    """
    params: Dict[str, str] = field(default_factory=dict)

    def register(self, value: str, key: Optional[str] = None) -> str:
        """Stores a new named parameter value.
        If not provided, also generates the parameter name.
        """
        key = f"p_{shorthash(value)}" if key is None else key
        self.params[key] = value
        return key
