from enum import Enum
from typing import Union

from pypika.terms import AggregateFunction, Term, Function

from tesseract_olap.schema.enums import MemberType


class ClickhouseDataType(Enum):
    """Lists the types of the data the user can expect to find in the associated
    column."""
    BOOLEAN = "Bool"
    DATE = "Date32"
    DATETIME = "DateTime64"
    TIMESTAMP = "UInt32"
    FLOAT32 = "Float32"
    FLOAT64 = "Float64"
    INT8 = "Int8"
    INT16 = "Int16"
    INT32 = "Int32"
    INT64 = "Int64"
    INT128 = "Int128"
    UINT8 = "UInt8"
    UINT16 = "UInt16"
    UINT32 = "UInt32"
    UINT64 = "UInt64"
    UINT128 = "UInt128"
    STRING = "String"

    @classmethod
    def from_membertype(cls, mt: MemberType):
        """Transforms a MemberType enum value into a ClickhouseDataType."""
        return next((item for item in cls if item.name == mt.name), cls.STRING)


class ArrayElement(Function):
    def __init__(
        self,
        array: Union[str, Term],
        n: Union[int, Term],
        alias: Union[str, None] = None,
    ) -> None:
        super(ArrayElement, self).__init__("arrayElement", array, n, alias=alias)


class Power(Function):
    def __init__(
        self,
        base: Union[int, Term],
        exp: Union[int, Term],
        alias: Union[str, None] = None,
    ):
        super(Power, self).__init__("pow", base, exp, alias=alias)


class AverageWeighted(AggregateFunction):
    def __init__(
        self,
        value_field: Union[str, Term],
        weight_field: Union[str, Term],
        alias: Union[str, None] = None,
    ):
        super().__init__("avgWeighted", value_field, weight_field, alias=alias)


class TopK(AggregateFunction):
    def __init__(
        self,
        amount: int,
        field: Union[str, Term],
        alias: Union[str, None] = None,
    ):
        super().__init__("topK(%d)" % amount, field, alias=alias)
