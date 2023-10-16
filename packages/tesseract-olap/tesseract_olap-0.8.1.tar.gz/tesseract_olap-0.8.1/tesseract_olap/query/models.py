"""Query-related internal structs module.

This module contains data-storing structs, used mainly on the query and backend
modules.
"""

import dataclasses
from typing import (Dict, FrozenSet, Iterable, NamedTuple, Optional, Set,
                    Tuple, Union)

from typing_extensions import Literal

from tesseract_olap.common import Array, Prim, shorthash
from tesseract_olap.schema import (DimensionTraverser, HierarchyTraverser,
                                   LevelTraverser, Measure, PropertyTraverser)

from .enums import (Comparison, LogicOperator, Membership, Order,
                    RestrictionAge, RestrictionScale)

NumericConstraint = Tuple[Union[Comparison, str], float]
MembershipConstraint = Tuple[Membership, Array[str]]
SingleFilterCondition = Tuple[NumericConstraint]
DoubleFilterCondition = Tuple[NumericConstraint, Literal["and", "or"], NumericConstraint]
FilterCondition = Union[
    SingleFilterCondition,
    Tuple[NumericConstraint, LogicOperator, NumericConstraint]
]


@dataclasses.dataclass(eq=False, frozen=True, order=False)
class CutIntent:
    """Filtering instructions for a qualitative value.

    Instances of this class are used to define cut parameters.
    Its values are directly inputted by the user, so should never be considered
    valid by itself.
    """
    level: str
    include_members: Set[Prim]
    exclude_members: Set[Prim]

    @classmethod
    def new(cls, level: str, incl: Iterable[Prim], excl: Iterable[Prim]):
        # TODO: enable compatibility for ranged-type include/exclude
        null_values = ("", ",")
        # The include/exclude sets are intended to be used as rules for the
        # composition of the query, so it's not needed to resolve them here.
        include = set(incl).difference(null_values)
        exclude = set(excl).difference(null_values)
        return cls(level=level, include_members=include, exclude_members=exclude)


@dataclasses.dataclass(eq=False, frozen=True, order=False)
class FilterIntent:
    """Filtering instructions for a quantitative value.

    Instances of this class are used to define filter parameters.
    Its values are directly inputted by the user, so should never be considered
    valid by itself.
    """

    field: str
    condition: FilterCondition

    @classmethod
    def new(
        cls,
        field: str,
        condition: Union[NumericConstraint, SingleFilterCondition, DoubleFilterCondition],
        *,
        and_: Optional[NumericConstraint] = None,
        or_: Optional[NumericConstraint] = None,
    ):
        def _numconst(comp: Tuple[str, float]) -> NumericConstraint:
            return Comparison.from_str(comp[0]), comp[1]

        if len(condition) == 3:
            cond1, oper, cond2 = condition
            cond = (_numconst(cond1), LogicOperator.from_str(oper), _numconst(cond2))
        else:
            constr = condition[0] if len(condition) == 1 else condition
            if and_ is not None:
                cond = (_numconst(constr), LogicOperator.AND, _numconst(and_))
            elif or_ is not None:
                cond = (_numconst(constr), LogicOperator.OR, _numconst(or_))
            else:
                cond = (_numconst(constr), )

        return cls(field=field, condition=cond)


class PaginationIntent(NamedTuple):
    """Pagination instructions for internal use."""
    limit: int = 0
    offset: int = 0

    @classmethod
    def from_str(cls, value: str):
        """Parses a string in format `int[,int]` into a Pagination tuple."""
        if value == "":
            raise ValueError("Invalid Pagination: no value provided")
        limit, offset = f"{value},0,0".split(",")[:2]

        if not limit.isnumeric():
            raise ValueError("Provided \"limit\" parameter is not an integer")
        if not offset.isnumeric():
            raise ValueError("Provided \"offset\" parameter is not an integer")

        return cls(limit=0 if limit is None else int(limit),
                   offset=0 if offset is None else int(offset))


class SortingIntent(NamedTuple):
    """Sorting instructions for internal use."""
    field: str
    order: Order

    @classmethod
    def new(cls, field: str, order: Union[Order, str, None]):
        """Creates a new SortingIntent object, accepting more diverse parameters.
        """
        order = order if isinstance(order, Order) else Order.from_str(order)
        return cls(field=field, order=order)

    @classmethod
    def from_str(cls, value: str):
        """Parses a string into a SortingIntent object."""
        if value == "":
            raise ValueError("Invalid Sorting: no value provided")
        field, order = f"{value}..".split(".")[:2]
        return cls.new(field, order)  # type: ignore


@dataclasses.dataclass(eq=True, frozen=True, order=False)
class TimeRestriction:
    """Time-axis filtering instructions for internal use.

    Instances of this class are used to define a time restriction over the
    resulting data. It must always contain both fields."""

    level: Union[str, RestrictionScale]
    age: RestrictionAge
    amount: int = 1
    is_full: bool = False

    @classmethod
    def from_str(cls, value: str):
        """Parses a string into a TimeRestriction object."""

        (level, *params) = value.split(".")

        gen_scale = (item for item in RestrictionScale if item.value == level)
        level = next(gen_scale, level)

        if "latest" in params or "last" in params:
            age = RestrictionAge.LATEST
        elif "oldest" in params or "earliest" in params:
            age = RestrictionAge.OLDEST
        else:
            raise ValueError(f"Can't parse an age for the data: '{params}'")

        try:
            amount = next(int(item) for item in params if item.isnumeric())
        except StopIteration:
            amount = 1

        full = "full" in params or "all" in params

        return cls(level, age, amount, full)


@dataclasses.dataclass(eq=True, frozen=True, order=False)
class HierarchyField:
    """Contains the parameters associated to a slicing operation on the data,
    based on a single Hierarchy from a Cube's Dimension.
    """
    dimension: "DimensionTraverser"
    hierarchy: "HierarchyTraverser"
    levels: Tuple["LevelField", ...]

    @property
    def cut_levels(self) -> Iterable["LevelField"]:
        return (item for item in self.levels if item.is_cut)

    @property
    def drilldown_levels(self) -> Iterable["LevelField"]:
        return (item for item in self.levels if item.is_drilldown)

    @property
    def deepest_level(self) -> "LevelField":
        """Returns the deepest LevelField requested in this Hierarchy, for this
        query operation."""
        # TODO: check if is needed to force this to use drilldowns only
        return self.levels[-1]

    @property
    def foreign_key(self) -> str:
        """Returns the column in the fact table of the Cube this Dimension
        belongs to, that matches the primary key of the items in the dim_table.
        """
        return self.dimension.foreign_key  # type: ignore

    @property
    def has_drilldowns(self) -> bool:
        """Verifies if any of the contained LevelFields is being used as a
        drilldown."""
        return any(self.drilldown_levels)

    @property
    def primary_key(self) -> str:
        """Returns the column in the dimension table for the parent Dimension,
        which is used as primary key for the whole set of levels in the chosen
        Hierarchy."""
        return self.hierarchy.primary_key

    @property
    def table(self):
        """Returns the table to use as source for the Dimension data. If not
        set, the data is stored directly in the fact table for the Cube."""
        return self.hierarchy.table


@dataclasses.dataclass(eq=True, frozen=True, order=False)
class LevelField:
    """Contains the parameters associated to the slice operation, specifying the
    columns each resulting group should provide to the output data.
    """
    level: "LevelTraverser"
    caption: Optional["PropertyTraverser"] = None
    is_drilldown: bool = False
    members_exclude: Set[str] = dataclasses.field(default_factory=set)
    members_include: Set[str] = dataclasses.field(default_factory=set)
    properties: FrozenSet["PropertyTraverser"] = dataclasses.field(default_factory=frozenset)
    time_restriction: Optional[TimeRestriction] = None

    @property
    def alias(self):
        """Returns a deterministic short hash of the name of the entity."""
        return shorthash(self.level.name + self.level.key_column)

    @property
    def is_cut(self) -> bool:
        return len(self.members_exclude) + len(self.members_include) > 0

    @property
    def key_column(self) -> str:
        return self.level.key_column

    @property
    def name(self):
        return self.level.name


@dataclasses.dataclass(eq=True, frozen=True, order=False)
class MeasureField:
    """MeasureField dataclass.

    Contains the parameters needed to filter the data points returned by the
    query operation from the server.
    """
    measure: "Measure"
    is_measure: bool = False
    with_ranking: Literal["asc", "desc", None] = None
    constraint1: Optional[NumericConstraint] = None
    constraint2: Optional[NumericConstraint] = None
    joint: LogicOperator = LogicOperator.AND

    @property
    def alias_name(self):
        """Returns a deterministic short hash of the name of the entity."""
        return shorthash(self.measure.name)

    @property
    def alias_key(self):
        """Returns a deterministic hash of the key column of the entity."""
        return shorthash(self.measure.key_column)

    @property
    def is_filter(self) -> bool:
        return self.constraint1 is not None

    @property
    def name(self) -> str:
        """Quick method to return the measure name."""
        return self.measure.name

    @property
    def aggregator_params(self) -> Dict[str, str]:
        """Quick method to retrieve the measure aggregator params."""
        return self.measure.aggregator.get_params()

    @property
    def aggregator_type(self) -> str:
        """Quick method to retrieve the measure aggregator type."""
        return str(self.measure.aggregator)

    def get_source(self):
        # TODO add locale compatibility
        """Quick method to obtain the source information of the measure."""
        return self.measure.annotations.get("source")
