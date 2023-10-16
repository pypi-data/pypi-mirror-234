from typing import Dict, List, Optional, Tuple, Union

from fastapi import Depends, Query, Request
from typing_extensions import Literal

from tesseract_olap.common import FALSEY_STRINGS, TRUTHY_STRINGS
from tesseract_olap.query import (DataRequest, DataRequestParams,
                                  MembersRequest, MembersRequestParams,
                                  NumericConstraint)

SingleFilterCondition = Tuple[NumericConstraint]
DoubleFilterCondition = Tuple[NumericConstraint, Literal["and", "or"], NumericConstraint]
FilterCondition = Union[SingleFilterCondition, DoubleFilterCondition]


def query_cuts_include(request: Request):
    """FastAPI Dependency to parse including cut parameters.

    Parses all URL Search Params whose key is capitalized, as cut definitions.
    Values are members' IDs, separated by commas.
    """
    return {key: value.split(",")
            for key, value in request.query_params.items()
            if key[0].isupper()}


def query_cuts_exclude(exclude: str = ""):
    """FastAPI Dependency to parse excluding cut parameters.

    The value is composed by multiple cut definitions separated by semicolons:
        `{value}` := `{cut_def};{cut_def...}`
    Where a single cut definition is composed by the Level name, colon, and the
    list of keys separated by commas:
        `{cut_def}` := `{name}:{key},{key...}`
        `{name}` : `str`, the name of the Level to apply the cut
        `{key}` : `str | int`, the members' ID values
    """
    return {key: value.split(",")
            for key, value in (
                item.split(":")[:2]
                for item in exclude.split(";")
                if item != ""
            )}


def _filter_parse_condition(value: str) -> NumericConstraint:
    comparison, scalar = value.split(".", 1)
    return comparison, float(scalar)


def _filter_parse(value: str) -> Tuple[str, Union[SingleFilterCondition, DoubleFilterCondition]]:
    field, condition = value.split(".", 1)
    if ".and." in condition:
        cond1, cond2 = condition.split(".and.")
        return field, (_filter_parse_condition(cond1), "and", _filter_parse_condition(cond2))
    if ".or." in condition:
        cond1, cond2 = condition.split(".or.")
        return field, (_filter_parse_condition(cond1), "or", _filter_parse_condition(cond2))
    return field, (_filter_parse_condition(condition), )


def query_filters(filters: Optional[str] = None):
    """FastAPI Dependency to parse filter parameters.
    """
    if filters is None:
        return {}

    return {field: condition for field, condition in (
        _filter_parse(item) for item in filters.split(",") if item != ""
    )}


def query_pagination(limit: Optional[str] = None):
    """FastAPI Dependency to parse pagination parameters.

    The shape of the parameter is composed by one integer, or two integers
    separated by a comma:
        `{value}` := `{limit}` | `{limit},{offset}`
    Where:
        `{limit}` : `int`, defines the max amount of items in the response data

        `{offset}` : `int`, defines the index of the first item in the full list
        where the list in the response data will start
    """
    if limit is not None:
        return tuple(int(i) for i in limit.split(",")[:2])


def query_parents(parents: str = ""):
    """FastAPI Dependency to parse parent drilldown call parameters.

    The shape for the value is:
        `{value}` := `{truthy}` | `{falsey}` | `{name},{name...}`
    Where:
        `{truthy}` : `Literal['1', 'true', 'on', 'y', 'yes']`,
        retrieves parents for all drilldowns in the request;

        `{falsey}` : `Literal['0', 'false', 'off', 'n', 'no', 'none', '']`,
        deactivates parents for all drilldowns in the request (default);

        `{name}` : `str`,
        the name of the specific drilldown(s) to get parents for.
    """
    if parents.lower() in FALSEY_STRINGS:
        return False
    if parents.lower() in TRUTHY_STRINGS:
        return True
    return parents.split(",")


def query_ranking(ranking: str = ""):
    """FastAPI Dependency to parse ranked results parameter.

    Values `""`, `"0"`, `"false"`, `"off"`, `"n"`, `"no"`, `"none"` are assumed `False`.
    Values `"1"`, `"true"`, `"on"`, `"y"`, `"yes"` are assumed `True`.
    Any other string is interpreted as comma-separated measure names. If right
    before the name there's a minus character (`-`), the ranking for that measure
    will be calculated in descending order, ascending otherwise.
    """
    if ranking.lower() in FALSEY_STRINGS:
        return False
    if ranking.lower() in TRUTHY_STRINGS:
        return True
    return {item.lstrip("-"): "desc" if item.startswith("-") else "asc"
            for item in ranking.split(",")}


def query_sorting(sort: Optional[str] = None):
    """FastAPI Dependency to parse sorting parameters.

    The shape for the value is:
        `{value}` := `{field}` | `{field}.{order}`
    Where:
        `{field}` : `str`, defines the field to use: a Measure or Property

        `{order}` : `Literal["asc", "desc"]`, defines the order to use

    The field will be resolved to a Measure first, then a Property.
    When `{order}` is not set, `"asc"` will be used by default.
    """
    if sort is None:
        return None
    params = sort.split(".")
    order = (params[1] if len(params) > 1 else "asc").lower()
    return params[0], order if order in ("asc", "desc") else "asc"


def dataquery_params(
    cube_name: str = Query(..., alias="cube"),
    drilldowns: str = Query(...),
    measures: str = Query(...),
    cuts_exclude: Dict[str, List[str]] = Depends(query_cuts_exclude),
    cuts_include: Dict[str, List[str]] = Depends(query_cuts_include),
    filters: Dict[str, FilterCondition] = Depends(query_filters),
    limit: Optional[Tuple[int, int]] = Depends(query_pagination),
    locale: Optional[str] = None,
    parents: Union[bool, List[str]] = Depends(query_parents),
    properties: Optional[str] = None,
    ranking: Union[bool, Dict[str, Literal["asc", "desc"]]] = Depends(query_ranking),
    sorting: Optional[Tuple[str, Literal["asc", "desc"]]] = Depends(query_sorting),
    time: Optional[str] = None,
):
    """FastAPI Dependency to parse parameters into a DataRequest object.
    """
    params: DataRequestParams = {
        "drilldowns": [item.strip() for item in drilldowns.split(",")],
        "measures": [item.strip() for item in measures.split(",")],
        "cuts_exclude": cuts_exclude,
        "cuts_include": cuts_include,
        "filters": filters,
        "parents": parents,
        "ranking": ranking,
    }

    if locale is not None:
        params["locale"] = locale

    if properties is not None:
        params["properties"] = properties.split(",")

    if time is not None:
        params["time"] = time

    if limit is not None:
        params["pagination"] = limit

    if sorting is not None:
        params["sorting"] = sorting

    return DataRequest.new(cube_name, params)


def membersquery_params(
    cube_name: str = Query(..., alias="cube"),
    level: str = Query(...),
    locale: Optional[str] = None,
    search: str = "",
    limit: Optional[Tuple[int, int]] = Depends(query_pagination),
):
    """FastAPI Dependency to parse parameters into a MembersRequest object.
    """
    params: MembersRequestParams = {
        "level": level,
    }

    if locale is not None:
        params["locale"] = locale

    if limit is not None:
        params["pagination"] = limit

    if search != "":
        params["search"] = search

    return MembersRequest.new(cube_name, params)
