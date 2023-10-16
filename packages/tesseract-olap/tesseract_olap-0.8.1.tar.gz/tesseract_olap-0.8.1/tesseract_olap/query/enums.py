from enum import Enum
from typing import Optional


class Comparison(str, Enum):
    """Comparison Enum.

    Defines the available value comparison operations.
    """
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    EQ = "eq"
    NEQ = "neq"

    @classmethod
    def from_str(cls, value: str):
        value = value.lower().strip()
        try:
            return next((item for item in cls if item == COMPARISON_SYMBOL.get(value, value)))
        except StopIteration:
            raise ValueError(f"Invalid Comparison value: {value}") from None


COMPARISON_SYMBOL = {
    ">": Comparison.GT,
    ">=": Comparison.GTE,
    "<": Comparison.LT,
    "<=": Comparison.LTE,
    "=": Comparison.EQ,
    "==": Comparison.EQ,
    "!=": Comparison.NEQ,
}


class Order(str, Enum):
    """Order direction Enum.

    Defines a direction to use in a sorting operation.
    """
    ASC = "asc"
    DESC = "desc"

    @classmethod
    def from_str(cls, value: Optional[str]):
        return next((item for item in cls if item == value), cls.ASC)


class Membership(Enum):
    """Membership Enum.

    Defines the membership of a value to a set."""
    IN = "in"
    NIN = "nin"

    @classmethod
    def from_str(cls, value: str):
        try:
            return next((item for item in cls if item.value == value))
        except StopIteration:
            raise ValueError(f"Invalid Membership value: {value}") from None


class LogicOperator(str, Enum):
    """Logical connector Enum.

    Defines logical operations between conditional predicates.
    """
    AND = "and"
    OR = "or"
    XOR = "xor"

    def __repr__(self) -> str:
        return f"LogicOperator.{self.name}"

    @classmethod
    def from_str(cls, value: str):
        try:
            return next((item for item in cls if item.value == value))
        except StopIteration:
            raise ValueError(f"Invalid LogicOperator value: {value}") from None


class RestrictionScale(str, Enum):
    YEAR = "year"
    QUARTER = "quarter"
    MONTH = "month"
    WEEK = "week"
    DAY = "day"

    @classmethod
    def from_str(cls, value: str):
        assert value != "", "Invalid RestrictionScale: no value provided"
        try:
            value = value.lower()
            return next((item for item in cls if item.value == value))
        except StopIteration:
            raise ValueError(f"Invalid RestrictionScale value: {value}") from None


class RestrictionAge(str, Enum):
    LATEST = "latest"
    OLDEST = "oldest"

    @classmethod
    def from_str(cls, value: str):
        assert value != "", "Invalid RestrictionAge: no value provided"
        try:
            value = value.lower()
            return next((item for item in cls if item.value == value))
        except StopIteration:
            raise ValueError(f"Invalid RestrictionAge value: {value}") from None
