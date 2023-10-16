from enum import Enum
from typing import Any, Optional, Sequence


class AggregatorType(Enum):
    """Lists the possible aggregation operations to perform on the data to
    return a measure."""
    SUM = "sum"
    COUNT = "count"
    AVERAGE = "avg"
    MAX = "max"
    MIN = "min"
    MODE = "mode"
    BASICGROUPEDMEDIAN = "basic_grouped_median"
    WEIGHTEDSUM = "weighted_sum"
    WEIGHTEDAVERAGE = "weighted_avg"
    REPLICATEWEIGHTMOE = "replicate_weight_moe"
    CALCULATEDMOE = "moe"
    WEIGHTEDAVERAGEMOE = "weighted_average_moe"

    @classmethod
    def from_str(cls, value: str):
        value = value.lower()
        try:
            return next((item for item in cls if item.value == value))
        except StopIteration:
            raise ValueError(f"Invalid AggregatorType value: {value}")


class DimensionType(Enum):
    """Lists the kinds of data a dimension is storing."""
    STANDARD = "standard"
    TIME = "time"
    GEO = "geo"

    @classmethod
    def from_str(cls, value: Optional[str]):
        if value is None:
            return cls.STANDARD
        value = value.lower()
        return next((item for item in cls if item.value == value), cls.STANDARD)


class MemberType(Enum):
    """Lists the types of the data the user can expect to find in the associated
    column."""
    BOOLEAN = "bool"
    DATE = "date"
    TIME = "time"
    DATETIME = "dttm"
    TIMESTAMP = "stmp"
    FLOAT32 = "f32"
    FLOAT64 = "f64"
    INT8 = "i8"
    INT16 = "i16"
    INT32 = "i32"
    INT64 = "i64"
    INT128 = "i128"
    UINT8 = "u8"
    UINT16 = "u16"
    UINT32 = "u32"
    UINT64 = "u64"
    UINT128 = "u128"
    STRING = "str"

    def get_caster(self):
        if self in (
            MemberType.INT8, MemberType.INT16, MemberType.INT32, MemberType.INT64, MemberType.INT128,
            MemberType.UINT8, MemberType.UINT16, MemberType.UINT32, MemberType.UINT64, MemberType.UINT128,
        ):
            return int
        if self in (MemberType.FLOAT32, MemberType.FLOAT64):
            return float
        if self == MemberType.BOOLEAN:
            return bool
        return str

    @classmethod
    def from_str(cls, value: Optional[str]):
        if value is None:
            return cls.INT64
        value = value.lower()
        return next((item for item in cls if item.value == value), cls.INT64)

    @classmethod
    def from_values(cls, values: Sequence[Any]):
        types = frozenset(type(value) for value in values)

        if len(types) == 1 and bool in types:
            return MemberType.BOOLEAN

        if float in types:
            return MemberType.FLOAT64

        if int in types:
            return cls.from_int_values(values)

        return MemberType.STRING

    @classmethod
    def from_int_values(cls, values: Sequence[int]):
        mini = min(values)
        maxi = max(values)

        if mini < 0:
            if mini < -(2**63) or maxi > 2**63-1:
                return MemberType.INT128
            elif mini < -(2**31) or maxi > 2**31-1:
                return MemberType.INT64
            elif mini < -(2**15) or maxi > 2**15-1:
                return MemberType.INT32
            elif mini < -128 or maxi > 127:
                return MemberType.INT16
            else:
                return MemberType.INT8
        else:
            if maxi > 2**64-1:
                return MemberType.UINT128
            elif maxi > 2**32-1:
                return MemberType.UINT64
            elif maxi > 65535:
                return MemberType.UINT32
            elif maxi > 255:
                return MemberType.UINT16
            else:
                return MemberType.UINT8
