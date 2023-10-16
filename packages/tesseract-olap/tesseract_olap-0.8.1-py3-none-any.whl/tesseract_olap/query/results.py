"""Result structs module

This module contains wrapper classes for the resulting data of queries obtained
for structs in the requests module.
"""

from dataclasses import dataclass, field
from typing import AsyncIterator, Optional

from tesseract_olap.common import AnyDict, Array

from .requests import DataRequest, MembersRequest


@dataclass(eq=False, order=False)
class DataResult:
    """Container class for results to :class:`DataRequest`."""
    first: Optional[AnyDict]
    iterator: AsyncIterator[AnyDict]
    sources: Array[AnyDict]
    query: DataRequest
    _use_iterator: bool = field(default=False, init=False, repr=False, compare=False)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._use_iterator:
            return await self.iterator.__anext__()

        self._use_iterator = True

        if self.first is None:
            raise StopAsyncIteration()

        return self.first


@dataclass(eq=False, order=False)
class MembersResult:
    """Container class for results to :class:`MembersRequest`."""
    first: Optional[AnyDict]
    iterator: AsyncIterator[AnyDict]
    query: MembersRequest
    _use_iterator: bool = field(default=False, init=False, repr=False, compare=False)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._use_iterator:
            return await self.iterator.__anext__()

        self._use_iterator = True

        if self.first is None:
            raise StopAsyncIteration()

        return self.first
