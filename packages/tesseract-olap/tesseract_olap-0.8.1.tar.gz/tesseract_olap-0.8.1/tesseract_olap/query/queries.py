"""Query-related data-handling models module.

This module contains data structs used to carry and compose objects used during
a Query. The elements are agnostic to the type of backend used, and its primary
purpose is organize and easily obtain the data needed for later steps.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from itertools import chain
from typing import List, Mapping, Optional, Set, Tuple, Union

import immutables as immu
from typing_extensions import Literal

from tesseract_olap.common import AnyDict
from tesseract_olap.schema import (CubeTraverser, DimensionTraverser,
                                   HierarchyTraverser, LevelTraverser, Measure,
                                   SchemaTraverser)

from .enums import LogicOperator, RestrictionScale
from .exceptions import InvalidEntityName, MissingMeasures
from .models import (CutIntent, HierarchyField, LevelField, MeasureField,
                     PaginationIntent, SortingIntent)
from .requests import DataRequest, MembersRequest


@dataclass(eq=False, order=False)
class DataQuery:
    """Internal DataQuery class.

    Contains all the schema-hydrated elements corresponding to a
    :class:`DataRequest`, but also joining properties related to the same
    columnar entities.
    """

    cube: "CubeTraverser"
    locale: str
    fields_qualitative: Tuple["HierarchyField", ...] = field(default_factory=tuple)
    fields_quantitative: Tuple["MeasureField", ...] = field(default_factory=tuple)
    options: Mapping[str, bool] = field(default_factory=dict)
    pagination: "PaginationIntent" = field(default_factory=PaginationIntent)
    parents: Union[bool, Set[str]] = False
    ranking: Mapping[str, Literal["asc", "desc"]] = field(default_factory=dict)
    sorting: Optional["SortingIntent"] = None

    @classmethod
    def from_request(cls, schema: "SchemaTraverser", request: "DataRequest"):
        """Generates a new :class:`Query` instance from the parameters defined
        in a :class:`DataRequest` object.

        If any of the parameters can't be found on the Schema, raises a derivate
        of the :class:`InvalidQuery` error.
        """
        cube = schema.get_cube(request.cube)

        return cls(
            cube=cube,
            fields_qualitative=_get_data_hierarfields(cube, request),
            fields_quantitative=_get_data_measurefields(cube, request),
            locale=schema.default_locale \
                   if request.locale is None else \
                   request.locale,
            options=request.options,
            pagination=request.pagination,
            parents=request.parents,
            ranking=_resolve_ranking(request),
            sorting=request.sorting,
        )

    def get_sources(self) -> Tuple[AnyDict, ...]:
        """Returns a sequence containing the sources for each measure in the Query.

        Only measures with a properly declared source will appear in this dict.
        """
        source = {
            "name": self.cube.name,
            "measures": [item.name for item in self.fields_quantitative if item.is_measure],
            "annotations": self.cube.annotations,
        }
        return (source,)


@dataclass(eq=False, order=False)
class MembersQuery:
    """Internal MembersQuery class."""

    cube: "CubeTraverser"
    hiefield: "HierarchyField"
    locale: str
    pagination: "PaginationIntent" = field(default_factory=PaginationIntent)
    search: Optional[str] = None

    @classmethod
    def from_request(cls, schema: "SchemaTraverser", request: "MembersRequest"):
        """Generates a new :class:`MembersQuery` instance from a user-provided
        :class:`MembersRequest` instance.
        """
        cube = schema.get_cube(request.cube)

        return cls(
            cube=cube,
            hiefield=_get_members_hierarfield(cube, request),
            locale=schema.default_locale \
                   if request.locale is None else \
                   request.locale,
            pagination=request.pagination,
            search=request.search,
        )


def _get_data_hierarfields(cube: "CubeTraverser", req: "DataRequest"):
    """Regroups query parameters related to a Level, to simplify later usage."""
    # we need a map with all possible levels, including the cube's shared dimensions
    level_map = immu.Map((level.name, (dimension, hierarchy, level))
                         for dimension in cube.dimensions
                         for hierarchy in dimension.hierarchies
                         for level in hierarchy.levels)

    drilldown_set = req.drilldowns
    property_set = req.properties
    caption_set = req.captions
    cut_map = {**req.cuts}

    with_parents = req.parents
    if isinstance(with_parents, bool):
        with_parents = drilldown_set if with_parents else set("")

    involved_levels = req.drilldowns.copy()
    involved_levels.update(item.level for item in req.cuts.values())

    time_level = None
    time_restr = req.time_restriction
    if time_restr is not None:
        granularity = time_restr.level
        time_level = (
            cube.get_time_level(granularity.value)
            if isinstance(granularity, RestrictionScale) else
            cube.get_time_level(granularity)
        )
        involved_levels.add(time_level.name)

    # Ensure all levels involved in the request don't break
    # the 'single dimension, same hierarchy' rule
    dimension_store: Mapping[DimensionTraverser, HierarchyTraverser] = {}
    hierarchy_store: Mapping[HierarchyTraverser, List[LevelTraverser]] = defaultdict(list)

    for name in involved_levels:
        dimension, hierarchy, level = level_map[name]
        if dimension_store.get(dimension, hierarchy) != hierarchy:
            raise ValueError(
                "Multiple Hierarchies from the same Dimension are being requested. "
                "Only a single Hierarchy can be used at a time for a query."
            )
        dimension_store[dimension] = hierarchy
        hierarchy_store[hierarchy].append(level)

    # Apply default members
    for dimension in cube.dimensions:
        # Get the relevant Hierarchy for each Dimension in the Cube
        hierarchy = dimension_store.get(dimension, dimension.default_hierarchy)

        # The default_member logic will be applied only if the
        # (dimension, hierarchy) is not present in the user request
        levels = hierarchy_store[hierarchy]
        if len(levels) > 0:
            continue

        # Store the default hierarchy for the SQL subset filter
        dimension_store[dimension] = hierarchy

        default_member = hierarchy.default_member
        if default_member is None:
            continue

        level, member = default_member
        levels.append(level)
        cut_map[level.name] = CutIntent.new(level.name, incl=[member], excl=[])

    def _compose_field(level: "LevelTraverser", is_drilldown: bool) -> "LevelField":
        """Capsules the logic to fill a LevelField instance with data from both
        a Drilldown and a Cut.
        """
        kwargs = {
            "is_drilldown": is_drilldown,
            "properties": frozenset(prop
                                    for prop in level.properties
                                    if prop.name in property_set),
            "caption": next((capt
                            for capt in level.properties
                            if capt.name in caption_set), None),
            "time_restriction": time_restr if time_level == level else None,
        }

        cut = cut_map.get(level.name)
        if cut is not None:
            kwargs["members_exclude"] = set(cut.exclude_members)
            kwargs["members_include"] = set(cut.include_members)

        return LevelField(level=level, **kwargs)

    def _resolve_fields(hierarchy: "HierarchyTraverser"):
        """Calculates the levels involved in the request, depending on the
        with_parent parameter.
        """
        involved_levels = hierarchy_store[hierarchy]
        fields: List[LevelField] = []

        parent_flag = False
        # iterations will be done in reverse to use a flag for parents
        for level in reversed(tuple(hierarchy.levels)):
            # if includes_parents, and a deeper level is drilldown,
            # or if it's explicitly a drilldown
            is_drilldown = parent_flag or level.name in drilldown_set
            # is_field means the level needs to be SELECTed
            # to be used as a foreign key for a drilldown or a cut
            is_field = is_drilldown or level in involved_levels
            if is_field:
                fields.append(_compose_field(level, is_drilldown))
            # if level is marked in parents, raise flag
            # TODO: can be improved
            parent_flag = parent_flag or (
                is_drilldown and level.name in with_parents
            )

        fields.reverse()
        return tuple(fields)

    return tuple(
        HierarchyField(dimension, hierarchy, levels=_resolve_fields(hierarchy))
        for dimension, hierarchy in (
            sorted(dimension_store.items(), key=lambda item: item[0].name)
        )
    )


def _get_data_measurefields(cube: "CubeTraverser", req: "DataRequest"):
    """Regroups query parameters related to a Measure, to simplify contextual use.
    """
    measure_set = req.measures

    ranking_flags = _resolve_ranking(req)

    measure_map = immu.Map(
        (item.name, item)
        for measure in cube.measure_map.values()
        for item in _yield_all_measures(measure)
    )

    try:
        involved_measures = set(measure_map[name] for name in chain(
            req.measures,
            (item.field for item in req.filters.values()),
        ))
    except KeyError as exc:
        raise InvalidEntityName("Measure", exc.args[0]) from None

    involved_submeasures = set(
        submeasure
        for measure in involved_measures
        for submeasure in measure.submeasures.values()
    )
    involved_measures.update(involved_submeasures)

    def _compose_field(measure: "Measure") -> "MeasureField":
        kwargs = {
            "is_measure": measure.name in measure_set,
            "constraint1": None,
            "with_ranking": None,
        }

        with_ranking = ranking_flags.get(measure.name)
        # Ranking is available for top level measures only
        if with_ranking and measure.name in cube.measure_map:
            kwargs["with_ranking"] = with_ranking

        fltr = req.filters.get(measure.name)
        if fltr is None:
            pass
        elif len(fltr.condition) == 1: # is (NumConstr)
            kwargs["constraint1"] = fltr.condition[0]
        elif len(fltr.condition) == 3: # is (NumConstr, LogicOp, NumConstr)
            kwargs["constraint1"] = fltr.condition[0]
            kwargs["joint"] = LogicOperator.from_str(fltr.condition[1])
            kwargs["constraint2"] = fltr.condition[2]

        return MeasureField(measure, **kwargs)

    return tuple(_compose_field(measure) for measure in involved_measures)


def _get_members_hierarfield(cube: "CubeTraverser", req: "MembersRequest"):
    """Regroups query parameters related to a Level, to simplify later usage."""
    level_name = req.level
    with_parents = req.options.get("parents", False)

    try:
        dimension, hierarchy, level = next((dimension, hierarchy, level)
                                           for dimension in cube.dimensions
                                           for hierarchy in dimension.hierarchies
                                           for level in hierarchy.levels
                                           if level.name == level_name)
    except StopIteration:
        raise InvalidEntityName("Level", level_name) from None

    if with_parents:
        levels = tuple(hierarchy.levels)
        last_index = levels.index(level)
        fields = tuple(LevelField(level) for level in levels[0:last_index])
    else:
        fields = LevelField(level),

    return HierarchyField(dimension, hierarchy, levels=fields)


def _yield_all_measures(measure: "Measure"):
    """Yields a Measure and all its Submeasures, up to one level of depth."""
    yield measure
    for submeasure in measure.submeasures.values():
        yield submeasure


@lru_cache(maxsize=1)
def _resolve_ranking(req: "DataRequest") -> Mapping[str, Literal["asc", "desc"]]:
    """Restructures the ranking parameter to be used in SQL building."""
    measure_set = req.measures

    # Resolve the hashmap of measures for the ranking request
    ranking_flags: Mapping[str, Literal["asc", "desc"]] = {}
    if req.ranking is True:
        ranking_flags = {item: "desc" for item in measure_set}
    elif isinstance(req.ranking, dict):
        ranking_flags = req.ranking

    # Check if the measures in the ranking request are in the requested measures
    rank_diff = set(ranking_flags.keys())
    rank_diff.difference_update(measure_set)
    if len(rank_diff) > 0:
        raise MissingMeasures("ranking", rank_diff)

    return ranking_flags
