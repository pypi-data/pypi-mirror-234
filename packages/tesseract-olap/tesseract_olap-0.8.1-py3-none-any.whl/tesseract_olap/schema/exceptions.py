from typing import Union

from lxml import etree

from tesseract_olap.common import BaseError


class XMLParseError(BaseError):
    """An error happened while trying to parse a XML Schema."""


class MalformedXML(XMLParseError):
    """An unexpected node was found."""
    def __init__(self, expected: str, actual: Union[str, etree._Element]) -> None:
        message = (
            "A node '{1}' was found while attempting to parse a '{0}'"
        ).format(expected, actual)
        super().__init__(message)


class InvalidXMLAttributeName(XMLParseError):
    """An invalid attribute was found in a node."""
    def __init__(self, node: str, node_name: str, attr: str) -> None:
        message = (
            "An attribute '{2}' was found while attempting to parse {0} '{1}'"
        ).format(node, node_name, attr)
        super().__init__(message)


class InvalidXMLAttributeValue(XMLParseError):
    """An invalid value was found in the attribute of a node."""
    def __init__(self, node: str, node_name: str, attr: str, value: str) -> None:
        message = (
            "An invalid value '{3}' for the '{2}' attribute was found while " +
            "trying to parse {0} '{1}'"
        ).format(node, node_name, attr, value)
        super().__init__(message)


class MissingXMLNode(XMLParseError):
    """A required child node is missing."""
    def __init__(self, node: str, node_name: str, child_node: str) -> None:
        message = (
            "A '{2}' child node is missing in {0} '{1}'"
        ).format(node, node_name, child_node)
        super().__init__(message)


class MissingXMLAttribute(XMLParseError):
    """A required attribute is not present."""
    def __init__(self, node: str, attr: str) -> None:
        message = (
            "A required attribute '{1}' is missing in a '{0}' node"
        ).format(node, attr)
        super().__init__(message)


class JSONParseError(BaseError):
    """An error happened while trying to parse a JSON Schema."""


class MalformedJSON(JSONParseError):
    """An unexpected object was found."""
    def __init__(self, expected: str) -> None:
        message = ""
        super().__init__(message)


class SchemaError(BaseError):
    """An error happened when validating the internal references in a schema."""


class MissingPropertyError(SchemaError):
    """A mandatory property couldn't be retrieved from a Shared/Usage entity
    combination."""
    def __init__(self, entity: str, name: str, attr: str):
        message = (
            "There's a missing '{2}' attribute in {0} '{1}'."
        ).format(entity, name, attr)
        super().__init__(message)


class DuplicatedNameError(SchemaError):
    """The name of a certain Entity that needs to be unique is duplicated across
    a single cube."""
    def __init__(self, entity: str, name: str):
        message = (
            "There's a duplicated {} with the name '{}'. "
            "Names for the same kind of entity must be unique across its cube."
        ).format(entity, name)
        super().__init__(message)


class EntityUsageError(SchemaError):
    """There's a declared Usage reference pointing to a non-existent shared
    Entity."""
    def __init__(self, entity: str, source: str) -> None:
        message = (
            "An usage reference for '{}' {} cannot be found."
        ).format(source, entity)
        super().__init__(message)
