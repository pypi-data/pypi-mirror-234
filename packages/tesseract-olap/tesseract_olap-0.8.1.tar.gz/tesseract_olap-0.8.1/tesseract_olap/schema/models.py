import logging
from dataclasses import dataclass, field
from typing import Iterable, List, Mapping, Optional, Sequence, Tuple, Union

import immutables as immu

from tesseract_olap.common import get_localization

from .aggregators import Aggregator, Count
from .enums import DimensionType, MemberType

logger = logging.getLogger(__name__)

# Named types
Annotations = Mapping[str, Optional[str]]
CaptionSet = Mapping[str, str]


@dataclass(eq=True, frozen=True)
class Schema:
    """Base Schema class."""

    name: str
    annotations: Annotations = field(default_factory=immu.Map)
    cube_map: Mapping[str, "Cube"] = field(default_factory=immu.Map)
    default_locale: str = "xx"
    shared_dimension_map: Mapping[str, "Dimension"] = field(default_factory=immu.Map)
    shared_table_map: Mapping[str, "InlineTable"] = field(default_factory=immu.Map)

    @classmethod
    def join(cls, *args: "Schema"):
        annotations = {}
        cube_map = {}
        shared_dimension_map = {}
        shared_table_map = {}

        for sch in args:
            annotations.update(sch.annotations)
            cube_map.update(sch.cube_map)
            shared_dimension_map.update(sch.shared_dimension_map)
            shared_table_map.update(sch.shared_table_map)

        return cls(
            name=next(item.name for item in args if item.name != ""),
            default_locale=next((item.default_locale for item in args), "xx"),
            annotations=annotations,
            cube_map=cube_map,
            shared_dimension_map=shared_dimension_map,
            shared_table_map=shared_table_map,
        )


@dataclass(eq=True, frozen=True, repr=False)
class AccessControl:
    public: bool = True
    rules: Mapping[str, bool] = field(default_factory=immu.Map)

    def __repr__(self) -> str:
        return 'Public' if self.public else 'Private(%d)' % len(self.rules)

    def is_authorized(self, roles: Iterable[str]) -> bool:
        rules = self.rules
        return self.public or any(rules.get(role, False) for role in roles)


@dataclass(eq=True, frozen=True, repr=False)
class InlineTable:
    name: str
    headers: Tuple[str, ...]
    types: Tuple[MemberType, ...]
    rows: List[Tuple[Union[str, float], ...]]

    def __repr__(self) -> str:
        return "{0.__class__.__name__}(name='{0.name}')".format(self)

    @staticmethod
    def infer_types(rows: Sequence[Tuple[Union[float, str], ...]]):
        return tuple(MemberType.from_values(column) for column in zip(*rows))


class Entity:
    name: str
    annotations: Annotations
    captions: CaptionSet
    acl: AccessControl = field(default_factory=AccessControl)

    def get_annotation(self, name: str) -> Optional[str]:
        """Retrieves an annotation for the entity.
        If the annotation is not defined, raises a :class:`KeyError`.
        """
        return self.annotations[name]

    def get_caption(self, locale: str = "xx") -> str:
        """Retrieves the caption of the entity for a certain locale.
        If the a caption hasn't been defined for said locale, will attempt to
        return the fallback caption, and if not defined either, will return the
        entity name.
        """
        caption = get_localization(self.captions, locale)
        return self.name if caption is None else caption

    def get_locale_available(self) -> List[str]:
        """Retrieves the list of locales for whose a caption has been defined in
        this entity.
        """
        return sorted(self.captions.keys())

    def is_authorized(self, role: Iterable[str]) -> bool:
        role = {role} if isinstance(role, str) else role
        return self.acl.is_authorized(role)


@dataclass(eq=True, frozen=True)
class Cube(Entity):
    name: str
    table: Union["InlineTable", "Table", str]
    acl: AccessControl = field(default_factory=AccessControl)
    annotations: Annotations = field(default_factory=immu.Map)
    captions: CaptionSet = field(default_factory=immu.Map)
    dimension_map: Mapping[str, Union["Dimension", "DimensionUsage"]] \
        = field(default_factory=immu.Map)
    measure_map: Mapping[str, "Measure"] = field(default_factory=immu.Map)
    subset_table: bool = False
    visible: bool = True


@dataclass(eq=True, frozen=True)
class Table:
    name: str
    primary_key: str
    schema: Optional[str] = None


@dataclass(eq=True, frozen=True)
class Dimension(Entity):
    name: str
    default_hierarchy: str
    annotations: Annotations = field(default_factory=immu.Map)
    captions: CaptionSet = field(default_factory=immu.Map)
    dim_type: DimensionType = DimensionType.STANDARD
    foreign_key: Optional[str] = None
    hierarchy_map: Mapping[str, "Hierarchy"] = field(default_factory=immu.Map)

    def get_default_hierarchy(self):
        return self.hierarchy_map[self.default_hierarchy]


@dataclass(eq=True, frozen=True)
class Hierarchy(Entity):
    name: str
    primary_key: str
    table: Union["InlineTable", "Table", str, None]
    annotations: Annotations = field(default_factory=immu.Map)
    captions: CaptionSet = field(default_factory=immu.Map)
    default_member: Optional[Tuple[str, str]] = None
    level_map: Mapping[str, "Level"] = field(default_factory=immu.Map)


@dataclass(eq=True, frozen=True)
class Level(Entity):
    name: str
    depth: int
    key_column: str
    annotations: Annotations = field(default_factory=immu.Map)
    captions: CaptionSet = field(default_factory=immu.Map)
    name_column_map: CaptionSet = field(default_factory=immu.Map)
    key_type: MemberType = MemberType.STRING
    property_map: Mapping[str, "Property"] = field(default_factory=immu.Map)

    def get_name_column(self, locale: str = "xx") -> Optional[str]:
        return get_localization(self.name_column_map, locale)

    def get_locale_available(self) -> List[str]:
        return sorted(set(self.captions.keys()).union(self.name_column_map.keys()))


@dataclass(eq=True, frozen=True)
class Property(Entity):
    name: str
    annotations: Annotations = field(default_factory=immu.Map)
    captions: CaptionSet = field(default_factory=immu.Map)
    key_column_map: immu.Map[str, str] = field(default_factory=immu.Map)
    key_type: MemberType = MemberType.STRING

    def get_key_column(self, locale: str = "xx") -> str:
        return get_localization(self.key_column_map, locale, force=True)

    def get_locale_available(self) -> List[str]:
        return sorted(set(self.captions.keys()).union(self.key_column_map.keys()))


@dataclass(eq=True, frozen=True)
class Measure(Entity):
    name: str
    key_column: str
    aggregator: Aggregator = field(default_factory=Count)
    annotations: Annotations = field(default_factory=immu.Map)
    captions: CaptionSet = field(default_factory=immu.Map)
    submeasures: Mapping[str, "Measure"] = field(default_factory=immu.Map)


class Usage(Entity):
    """Defines a base class for Usage entities, so the type checker can enforce
    a bound class as a parameter.
    """
    source: str


@dataclass(eq=True, frozen=True)
class DimensionUsage(Usage):
    """Establishes the usage of a :class:`Schema`-level :class:`SharedDimension`
    inside a :class:`Cube`.
    """
    name: str
    source: str
    foreign_key: str
    annotations: Annotations = field(default_factory=immu.Map)
    captions: CaptionSet = field(default_factory=immu.Map)
    hierarchy_map: Mapping[str, "HierarchyUsage"] = field(default_factory=immu.Map)


@dataclass(eq=True, frozen=True)
class HierarchyUsage(Usage):
    """Establishes the usage of a :class:`Hierarchy` defined in a
    :class:`SharedDimension`.
    """
    name: str
    source: str
    annotations: Annotations = field(default_factory=immu.Map)
    captions: CaptionSet = field(default_factory=immu.Map)
    level_map: Mapping[str, "LevelUsage"] = field(default_factory=immu.Map)


@dataclass(eq=True, frozen=True)
class LevelUsage(Usage):
    """Establishes the usage of a :class:`Level` defined in a :class:`Hierarchy`
    under a :class:`SharedDimension`.
    """
    name: str
    source: str
    annotations: Annotations = field(default_factory=immu.Map)
    captions: CaptionSet = field(default_factory=immu.Map)
    property_map: Mapping[str, "PropertyUsage"] = field(default_factory=immu.Map)


@dataclass(eq=True, frozen=True)
class PropertyUsage(Usage):
    """Establishes the usage of a :class:`Property` defined in a :class:`Level`
    under a :class:`SharedDimension`.
    """
    name: str
    source: str
    annotations: Annotations = field(default_factory=immu.Map)
    captions: CaptionSet = field(default_factory=immu.Map)
