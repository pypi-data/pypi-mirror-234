import logging
from functools import lru_cache
from itertools import chain
from typing import (TYPE_CHECKING, Generic, Iterable, Iterator, List, Mapping,
                    Optional, OrderedDict, Set, TypeVar, Union)

from tesseract_olap.common import T, get_localization
from tesseract_olap.query.exceptions import (InvalidEntityName,
                                             TimeDimensionUnavailable,
                                             TimeScaleUnavailable)

from .enums import DimensionType, MemberType
from .exceptions import (DuplicatedNameError, EntityUsageError,
                         MissingPropertyError)
from .models import (Annotations, CaptionSet, Cube, Dimension, DimensionUsage,
                     Entity, Hierarchy, HierarchyUsage, InlineTable, Level,
                     LevelUsage, Measure, Property, PropertyUsage, Schema,
                     Table, Usage)

if TYPE_CHECKING:
    from tesseract_olap.query import RequestWithRoles

logger = logging.getLogger(__name__)

EntityType = TypeVar("EntityType", bound=Entity)
UsageType = TypeVar("UsageType", bound=Usage)


class SchemaTraverser(Mapping[str, "CubeTraverser"]):
    """Wrapper class for Schema model, to generate the relationships between the
    shared entities and their usages.
    """

    def __init__(self, schema: "Schema"):
        self.schema = schema
        self.cube_map = OrderedDict(
            (name, CubeTraverser(cube,
                                 dimension_map=schema.shared_dimension_map,
                                 table_map=schema.shared_table_map))
            for name, cube in schema.cube_map.items()
        )

    def __len__(self) -> int:
        return len(self.cube_map)

    def __getitem__(self, key: str) -> "CubeTraverser":
        return self.get_cube(key)

    def __iter__(self) -> Iterator[str]:
        return iter(self.cube_map)

    @property
    def default_locale(self):
        return self.schema.default_locale

    def get_cube(self, cube_name: str) -> "CubeTraverser":
        try:
            return self.cube_map[cube_name]
        except KeyError:
            raise InvalidEntityName("Cube", cube_name) from None

    def get_locale_available(self) -> List[str]:
        locales = set()
        for item in self.cube_map.values():
            locales.update(item.get_locale_available())
        # TODO: add from shared_dimension_map and shared_table_map
        locales.discard("xx")
        locales.add(self.schema.default_locale)
        return sorted(locales)

    def get_public_schema(self, roles: List[str] = [], locale: Optional[str] = None):
        """Generates a JSON-encodeable schema describing this entity."""
        default_locale = self.schema.default_locale
        locale = default_locale if locale is None else locale
        return {
            "name": self.schema.name,
            # "locales": self.get_locale_available(),
            "default_locale": default_locale,
            "cubes": [cube.get_public_schema(locale)
                      for cube in self.cube_map.values()
                      if cube.visible and cube.is_authorized(roles)],
            "annotations": self.schema.annotations,
        }

    def is_authorized(self, request: "RequestWithRoles") -> bool:
        """Validates a request has enough permissions to be executed."""
        return self.get_cube(request.cube).is_authorized(request.roles)

    def validate(self):
        """Performs some verifications on the resulting data structure, after
        parsing the schema file."""

        def validate_unique_names(nameset: Set[str], item: "EntityUsageTraverser"):
            if item.name in nameset:
                origin = item._entity if item._usage is None else item._usage
                raise DuplicatedNameError(type(origin).__name__, item.name)
            nameset.add(item.name)

        for cube in self.cube_map.values():
            levelset = set()
            propsset = set()

            for level in cube.levels:
                validate_unique_names(levelset, level)
                for prop in level.properties:
                    validate_unique_names(propsset, prop)


class CubeTraverser:
    """Wrapper class for the :class:`Cube` model, that establishes the
    relationships between its usages and their source shared entities.

    The relationships are made via the :class:`EntityUsageTraverser` subclasses,
    initialized upon creation.
    """

    _cube: "Cube"
    _dimension_map: Mapping[str, "DimensionTraverser"]
    _table: Union["Table", "InlineTable"]
    annotations: Annotations
    captions: CaptionSet
    measure_map: Mapping[str, "Measure"]
    name: str
    subset_table: bool
    visible: bool

    def __init__(
        self,
        cube: "Cube",
        *,
        dimension_map: Mapping[str, "Dimension"],
        table_map: Mapping[str, "InlineTable"],
    ) -> None:
        self._cube = cube
        self._dimension_map = OrderedDict(
            (name, DimensionTraverser(item, table_map=table_map)
                   if isinstance(item, Dimension) else
                   DimensionTraverser(
                       get_shared_entity(dimension_map, item.source), item,
                       table_map=table_map))
            for name, item in cube.dimension_map.items()
        )
        self._table = table_map[cube.table] \
                      if isinstance(cube.table, str) else \
                      cube.table

    def __repr__(self) -> str:
        return f"CubeTraverser(name='{self._cube.name}', table={self.table})"

    def __getattr__(self, _name: str):
        return getattr(self._cube, _name)

    @property
    def table(self) -> Union["Table", "InlineTable"]:
        return self._table

    @property
    def measures(self) -> Iterable["Measure"]:
        return self._cube.measure_map.values()

    @property
    def dimensions(self) -> Iterable["DimensionTraverser"]:
        return self._dimension_map.values()

    @property
    def time_dimensions(self) -> Iterable["DimensionTraverser"]:
        return (item
                for item in self.dimensions
                if item.dim_type == DimensionType.TIME)

    @property
    def hierarchies(self) -> Iterable["HierarchyTraverser"]:
        return chain(*(item.hierarchies for item in self.dimensions))

    @property
    def levels(self) -> Iterable["LevelTraverser"]:
        return chain(*(item.levels for item in self.dimensions))

    @property
    def time_levels(self) -> Iterable["LevelTraverser"]:
        """Returns a generator that yields all Levels from a TIME Dimension under
        this Cube."""
        return chain(*(item.levels for item in self.time_dimensions))

    @property
    def properties(self) -> Iterable["PropertyTraverser"]:
        """Returns a generator that yields all Properties under this Cube."""
        return chain(*(item.properties for item in self.dimensions))

    def get_annotation(self, name: str) -> Optional[str]:
        return self._cube.get_annotation(name)

    def get_caption(self, locale: str = "xx") -> str:
        return self._cube.get_caption(locale)

    def get_locale_available(self) -> List[str]:
        """Returns a list of strings containing the locale code keys available
        for captions in entities inside this :class:`Cube`."""
        locales = set(self.captions.keys())
        for item in self.dimensions:
            locales.update(item.get_locale_available())
        for item in self.measures:
            locales.update(item.get_locale_available())
        return sorted(locales)

    def get_measure(self, name: str) -> "Measure":
        """Attempts to retrieve a Measure by its name.

        Raises :class:`InvalidEntityName` if the entity can't be found.
        """
        try:
            return self._cube.measure_map[name]
        except KeyError:
            raise InvalidEntityName("Measure", name) from None

    def get_dimension(self, name: str) -> "DimensionTraverser":
        """Attempts to retrieve a Dimension by its name.

        Raises :class:`InvalidEntityName` if the entity can't be found.
        """
        try:
            return self._dimension_map[name]
        except KeyError:
            raise InvalidEntityName("Dimension", name) from None

    def get_hierarchy(self, name: str) -> "HierarchyTraverser":
        """Attempts to retrieve a Hierarchy by its name.

        Raises :class:`InvalidEntityName` if the entity can't be found.
        """
        try:
            return next(item for item in self.hierarchies if item.name == name)
        except StopIteration:
            raise InvalidEntityName("Hierarchy", name) from None

    def get_level(self, name: str) -> "LevelTraverser":
        """Attempts to retrieve a Level by its name.

        Raises :class:`InvalidEntityName` if the entity can't be found.
        """
        try:
            return next(item for item in self.levels if item.name == name)
        except StopIteration:
            raise InvalidEntityName("Level", name) from None

    @lru_cache(maxsize=5)
    def get_time_level(self, scale: str) -> "LevelTraverser":
        """Attempts to return a Level from a TIME-type :class:`Dimension` that
        matches the name with a time scale name.

        Raises :class:`TimeDimensionUnavailable` if the :class:`Cube` doesn't
        contain a TIME-type :class:`Dimension`, and :class:`TimeScaleUnavailable`
        if the time scale requested is not available in the :class:`Dimension`.
        """
        dimension = None

        for dimension in self.time_dimensions:
            exact_match = next((item for item in dimension.levels
                               if item.name == scale), None)
            if exact_match is not None:
                return exact_match

        if dimension is None:
            raise TimeDimensionUnavailable(self._cube.name)

        for dimension in self.time_dimensions:
            substr_match = next((item for item in dimension.levels
                                if scale in item.name.lower()), None)
            if substr_match is not None:
                return substr_match

        raise TimeScaleUnavailable(self._cube.name, scale)

    def get_property(self, name: str) -> "PropertyTraverser":
        """Attempts to retrieve a Property by its name.

        Raises :class:`InvalidEntityName` if the entity can't be found.
        """
        try:
            return next(item for item in self.properties if item.name == name)
        except StopIteration:
            raise InvalidEntityName("Property", name) from None

    @lru_cache(maxsize=1)
    def get_public_schema(self, locale: str):
        """Generates a JSON-encodeable schema describing this entity."""
        return {
            "name": self.name,
            "caption": self._cube.get_caption(locale),
            "dimensions": [
                item.get_public_schema(locale)
                for item in self.dimensions
            ],
            "measures": [
                {
                    "name": measure.name,
                    "caption": measure.get_caption(locale),
                    "aggregator": {
                        "name": str(measure.aggregator),
                    },
                    "attached": [
                        {
                            "name": submsr.name,
                            "caption": submsr.get_caption(locale),
                            "aggregator": str(submsr.aggregator),
                        }
                        for submsr in measure.submeasures.values()
                    ],
                    "annotations": measure.annotations,
                }
                for measure in self.measures
            ],
            "annotations": self._cube.annotations,
        }

    def is_authorized(self, roles: Iterable[str]):
        return self._cube.is_authorized(roles)


class EntityUsageTraverser(Generic[EntityType, UsageType]):
    """Wrapper class to unify an usage with its entity.

    Its properties are looked on the usage, then on the entity if not found.
    The usage instance is optional, as this wrapper also standardizes the
    properties and traversing methods across entities in the codebase.
    """

    _entity: EntityType
    _usage: Optional[UsageType]

    def __init__(self, entity: EntityType, usage: Optional[UsageType] = None):
        self._entity = entity
        self._usage = usage

    def __contains__(self, item: Union[EntityType, UsageType]) -> bool:
        return item == self._entity or item == self._usage

    def __dir__(self) -> Iterable[str]:
        return sorted(set(dir(self._entity) + dir(self)))

    def __getattr__(self, name: str):
        return getattr(self._entity, name)

    def __repr__(self) -> str:
        return "{}(name='{}')".format(self.__class__.__name__, self.name)

    @property
    def name(self) -> str:
        """Returns the new name given by the usage reference, or the original
        name of the entity if not defined."""
        return self._entity.name if self._usage is None else self._usage.name

    @property
    def annotations(self) -> Annotations:
        """Returns a dict containing the combined annotations from the original
        entity and its usage, if defined."""
        if self._usage is None:
            return self._entity.annotations
        return {**self._entity.annotations, **self._usage.annotations}

    @property
    def captions(self) -> CaptionSet:
        """Returns a dict containing the combined captions from the original
        entity and its usage, if defined."""
        if self._usage is None:
            return self._entity.captions
        return {**self._entity.captions, **self._usage.captions}

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


class DimensionTraverser(EntityUsageTraverser[Dimension, DimensionUsage]):
    """Allows seamless aliasing of values between a Dimension and a DimensionUsage."""

    hierarchy_map: Mapping[str, "HierarchyTraverser"]
    dim_type: DimensionType

    def __init__(
        self,
        entity: "Dimension",
        usage: Optional["DimensionUsage"] = None,
        *,
        table_map: Mapping[str, "InlineTable"] = {},
    ) -> None:
        super().__init__(entity, usage)

        if usage is None or len(usage.hierarchy_map) == 0:
            self.hierarchy_map = OrderedDict(
                (name, HierarchyTraverser(item, table_map=table_map))
                for name, item in entity.hierarchy_map.items()
            )
        else:
            self.hierarchy_map = OrderedDict(
                (name, HierarchyTraverser(
                    entity.hierarchy_map[item.source], item, table_map=table_map
                ))
                for name, item in usage.hierarchy_map.items()
            )

    @property
    def foreign_key(self) -> str:
        """Returns the foreign key for this Dimension."""
        # A DimensionTraverser represents PrivateDimension or DimensionUsage,
        # and the foreign_key property must be present in both, final value
        # depends solely on self._usage presence.
        if self._usage is not None:
            return self._usage.foreign_key
        if self._entity.foreign_key is None:  # should be unreachable, but checks types
            raise MissingPropertyError("Dimension", self.name, "foreign_key")
        return self._entity.foreign_key

    @property
    def default_hierarchy(self) -> "HierarchyTraverser":
        hie = self._entity.get_default_hierarchy()
        if self._usage is None:
            return self.hierarchy_map[hie.name]
        try:
            # find the HierarchyTraverser that references the default Hierarchy
            return next(item for item in self.hierarchies if hie in item)
        except StopIteration:
            return next(iter(self.hierarchies))

    @property
    def hierarchies(self) -> Iterable["HierarchyTraverser"]:
        """Returns a generator that yields all Hierarchies under this Dimension."""
        return self.hierarchy_map.values()

    @property
    def levels(self) -> Iterable["LevelTraverser"]:
        """Returns a generator that yields all Levels under this Dimension."""
        return chain(*(item.levels for item in self.hierarchies))

    @property
    def properties(self) -> Iterable["PropertyTraverser"]:
        """Returns a generator that yields all Properties under this Dimension."""
        return chain(*(item.properties for item in self.hierarchies))

    def get_hierarchy(self, name: str) -> "HierarchyTraverser":
        """Retrieves a Hierarchy from this Dimension by its name.
        Raises :class:`InvalidEntityName` if the Hierarchy can't be found.
        """
        try:
            return next(item for item in self.hierarchies if item.name == name)
        except StopIteration:
            raise InvalidEntityName("Hierarchy", name) from None

    def get_level(self, name: str) -> "LevelTraverser":
        """Retrieves a Level from this Dimension by its name.
        Raises :class:`InvalidEntityName` if the Level can't be found.
        """
        try:
            return next(item for item in self.levels if item.name == name)
        except StopIteration:
            raise InvalidEntityName("Level", name) from None

    def get_property(self, name: str) -> "PropertyTraverser":
        """Retrieves a Property from this Dimension by its name.
        Raises :class:`InvalidEntityName` if the Property can't be found.
        """
        try:
            return next(item for item in self.properties if item.name == name)
        except StopIteration:
            raise InvalidEntityName("Property", name) from None

    def get_public_schema(self, locale: str):
        """Generates a JSON-encodeable schema describing this entity."""
        return {
            "name": self.name,
            "caption": self.get_caption(locale),
            "type": self.dim_type.value,
            "hierarchies": [
                item.get_public_schema(locale) for item in self.hierarchies
            ],
            "default_hierarchy": self._entity.default_hierarchy,
            "annotations": self.annotations,
        }


class HierarchyTraverser(EntityUsageTraverser[Hierarchy, HierarchyUsage]):
    """Allows seamless aliasing of values between a Hierarchy and a HierarchyUsage."""

    level_map: Mapping[str, "LevelTraverser"]
    primary_key: str
    # `table` might be `None` if intended to use foreign key as value, like "Year"
    table: Union["Table", "InlineTable", None]

    def __init__(
        self,
        entity: "Hierarchy",
        usage: Optional["HierarchyUsage"] = None,
        *,
        table_map: Mapping[str, "InlineTable"],
    ) -> None:
        super().__init__(entity, usage)

        self.table = (
            table_map[entity.table] if isinstance(entity.table, str) else entity.table
        )

        if usage is None or len(usage.level_map) == 0:
            self.level_map = OrderedDict(
                (name, LevelTraverser(item)) for name, item in entity.level_map.items()
            )
        else:
            self.level_map = OrderedDict(
                (name, LevelTraverser(entity.level_map[item.source], item))
                for name, item in usage.level_map.items()
            )

    @property
    def levels(self) -> Iterable["LevelTraverser"]:
        """Returns a generator that yields all Levels under this Hierarchy."""
        return self.level_map.values()

    @property
    def properties(self) -> Iterable["PropertyTraverser"]:
        """Returns a generator that yields all Properties under this Hierarchy."""
        return chain(*(item.properties for item in self.levels))

    @property
    def default_member(self):
        """Returns a tuple containing a Level and a default member ID, to restrict
        the data used in queries.
        """
        if self._entity.default_member is None:
            return None

        level_name, member = self._entity.default_member
        level = self.get_level(level_name)
        caster = level.key_type.get_caster()
        return level, caster(member)

    def get_level(self, name: str) -> "LevelTraverser":
        """Retrieves a Level from this Cube by its name."""
        try:
            return next(item for item in self.levels if item.name == name)
        except StopIteration:
            raise InvalidEntityName("Level", name) from None

    def get_property(self, name: str) -> "PropertyTraverser":
        """Retrieves a Property from this Cube by its name."""
        try:
            return next(item for item in self.properties if item.name == name)
        except StopIteration:
            raise InvalidEntityName("Property", name) from None

    def get_public_schema(self, locale: str):
        """Generates a JSON-encodeable schema describing this entity."""
        return {
            "name": self.name,
            "caption": self.get_caption(locale),
            "levels": [item.get_public_schema(locale) for item in self.levels],
            "annotations": self.annotations,
        }


class LevelTraverser(EntityUsageTraverser[Level, LevelUsage]):
    """Allows seamless aliasing of values between a Level and a LevelUsage."""

    depth: int
    key_column: str
    key_type: MemberType
    name: str
    property_map: Mapping[str, "PropertyTraverser"]

    def __init__(self, entity: "Level", usage: Optional["LevelUsage"] = None):
        super().__init__(entity, usage)

        if usage is None or len(usage.property_map) == 0:
            self.property_map = OrderedDict(
                (name, PropertyTraverser(item))
                for name, item in entity.property_map.items()
            )
        else:
            self.property_map = OrderedDict(
                (name, PropertyTraverser(entity.property_map[item.source], item))
                for name, item in usage.property_map.items()
            )

    @property
    def type_caster(self):
        return self.key_type.get_caster()

    @property
    def properties(self) -> Iterable["PropertyTraverser"]:
        """Returns a generator that yields all Properties under this Level."""
        return self.property_map.values()

    def get_name_column(self, locale: str = "xx") -> Union[str, None]:
        return self._entity.get_name_column(locale)

    def get_public_schema(self, locale: str):
        """Generates a JSON-encodeable schema describing this entity."""
        return {
            "name": self.name,
            "caption": self.get_caption(locale),
            "properties": [item.get_public_schema(locale) for item in self.properties],
            "annotations": self.annotations,
        }


class PropertyTraverser(EntityUsageTraverser[Property, PropertyUsage]):
    """Allows seamless aliasing of values between a Property and a PropertyUsage."""

    def get_key_column(self, locale: str = "xx"):
        """Returns the matching `key_column` of this Property for a certain locale."""
        return self._entity.get_key_column(locale)

    def get_public_schema(self, locale: str):
        """Generates a JSON-encodeable schema describing this entity."""
        return {
            "name": self.name,
            "caption": self.get_caption(locale),
            "type": self.key_type.value,
            "annotations": self.annotations,
        }


def get_shared_entity(shared_map: Mapping[str, T], name: str) -> T:
    try:
        return shared_map[name]
    except KeyError:
        raise EntityUsageError(name, "SharedDimension") from None
