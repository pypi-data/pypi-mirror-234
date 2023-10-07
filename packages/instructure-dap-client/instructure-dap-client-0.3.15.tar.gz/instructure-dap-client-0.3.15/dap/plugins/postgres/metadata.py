import re
import typing
from typing import Any, Dict, List, Optional, Union

import sqlalchemy
from dap.api import DAPClientError
from dap.conversion_nonperf import create_value_converter
from dap.dap_types import VersionedSchema
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.sql.type_api import TypeEngine
from strong_typing.core import JsonType, Schema

SqlAlchemyType = Union[
    sqlalchemy.BigInteger,
    sqlalchemy.Integer,
    sqlalchemy.SmallInteger,
    sqlalchemy.Float,
    sqlalchemy.Double,
    sqlalchemy.Enum,
    sqlalchemy.TIMESTAMP,
    sqlalchemy.String,
    sqlalchemy.JSON,
    sqlalchemy.Boolean,
    sqlalchemy.ARRAY,
    sqlalchemy.Uuid,
    INET,
]


def get_nested(schema: Schema, keys: List[str]) -> Dict[str, JsonType]:
    nested_value = typing.cast(Dict[str, JsonType], schema)
    for key in keys:
        nested_value = typing.cast(Dict[str, JsonType], nested_value[key])

    return nested_value


def get_reference(
    schema: Schema, reference: str, table_name: str
) -> Dict[str, JsonType]:
    valid_ref = re.search(r"^#(/\w+)+", reference)
    if not valid_ref:
        raise ReferenceError(reference, table_name)
    return get_nested(schema, reference.split("/")[1:])


def resolve_ref(schema: Schema, property_schema: Schema, table_name: str) -> Schema:
    if "oneOf" in property_schema:
        oneOfSchema = typing.cast(List[JsonType], property_schema["oneOf"])
        for index, item in enumerate(oneOfSchema):
            oneOfElement = typing.cast(Dict[str, JsonType], item)
            if "$ref" in oneOfElement:
                ref = typing.cast(str, oneOfElement["$ref"])
                oneOfSchema[index] = get_reference(schema, ref, table_name)

    if "$ref" in property_schema:
        ref = typing.cast(str, property_schema["$ref"])
        property_schema = get_reference(schema, ref, table_name)

    return property_schema


def match_type(
    schema: Schema, namespace: str, table_name: str, prop_name: str
) -> TypeEngine[Any]:
    detected_type: Optional[SqlAlchemyType] = None

    if "oneOf" in schema:
        oneOfSchema = typing.cast(List[JsonType], schema["oneOf"])
        all_ip = True
        for item in oneOfSchema:
            oneOfElement = typing.cast(Dict[str, JsonType], item)
            if oneOfElement["type"] != "string":
                raise OneOfTypeSchemaError(table_name)
            if not "format" in oneOfElement:
                all_ip = False
            elif oneOfElement["format"] != "ipv4" and oneOfElement["format"] != "ipv6":
                all_ip = False
        if all_ip:
            return INET()
        return sqlalchemy.String()

    if "type" not in schema:
        raise NoTypeSpecifiedError(table_name, prop_name)

    type_name = schema["type"]

    if type_name == "integer":
        if "enum" in schema:
            enum_int_items = typing.cast(List[int], schema["enum"])
            if min(enum_int_items) >= -(2**15) and max(enum_int_items) <= 2**15 - 1:
                detected_type = sqlalchemy.SmallInteger()
            elif (
                min(enum_int_items) >= -(2**31) and max(enum_int_items) <= 2**31 - 1
            ):
                detected_type = sqlalchemy.Integer()
            else:
                detected_type = sqlalchemy.BigInteger()
        elif schema["format"] == "int64":
            detected_type = sqlalchemy.BigInteger()
        elif schema["format"] == "int32":
            detected_type = sqlalchemy.Integer()
        elif schema["format"] == "int16":
            detected_type = sqlalchemy.SmallInteger()

    elif type_name == "number":
        if "format" not in schema:
            detected_type = sqlalchemy.Float()

        elif schema["format"] == "float64":
            detected_type = sqlalchemy.Double()

    elif type_name == "string":
        if "enum" in schema:
            enum_name = f"{table_name}__{prop_name}"
            enum_items = typing.cast(List[str], schema["enum"])
            detected_type = sqlalchemy.Enum(
                *enum_items, name=enum_name, create_type=True, schema=namespace
            )

        elif "format" in schema and schema["format"] == "date-time":
            detected_type = sqlalchemy.TIMESTAMP(timezone=False)

        elif "format" in schema and schema["format"] == "uuid":
            detected_type = sqlalchemy.Uuid()

        elif "format" in schema and (
            schema["format"] == "ipv4" or schema["format"] == "ipv6"
        ):
            detected_type = INET()

        elif "maxLength" in schema:
            max_length = typing.cast(int, schema["maxLength"])
            detected_type = sqlalchemy.String(length=max_length)
        else:
            detected_type = sqlalchemy.String()

    elif type_name == "object":
        detected_type = sqlalchemy.JSON()

    elif type_name == "boolean":
        detected_type = sqlalchemy.Boolean()

    elif type_name == "array":
        if "items" not in schema:
            raise NoArrayItemTypeSpecifiedError(table_name, prop_name)

        items_schema = typing.cast(Schema, schema["items"])
        detected_type = sqlalchemy.ARRAY(
            match_type(items_schema, namespace, table_name, prop_name)
        )

    if detected_type is None:
        raise UnrecognizedTypeError(table_name, prop_name)

    return detected_type


def get_comment(schema: Schema) -> str:
    comm = schema.get("description", "")
    if type(comm) != str:
        raise NoStringDescriptionError

    return comm


def get_default(schema: Schema, namespace: str, table_name: str, prop_name: str) -> Any:
    raw_default_value = schema.get("default")
    value_type = match_type(schema, namespace, table_name, prop_name)
    converter = create_value_converter(value_type)
    return converter(raw_default_value)


class DAPSchemaParsingError(DAPClientError):
    pass


class NoStringDescriptionError(DAPSchemaParsingError):
    def __init__(self) -> None:
        super().__init__("`description` of property in schema must be a string")


class UnrecognizedTypeError(DAPSchemaParsingError):
    def __init__(self, table_name: str, prop_name: str) -> None:
        super().__init__(f"Cannot find Column type for {table_name}.{prop_name}")


class NoArrayItemTypeSpecifiedError(DAPSchemaParsingError):
    def __init__(self, table_name: str, prop_name: str) -> None:
        super().__init__(
            f"No item type is specified for array type in {table_name}.{prop_name}"
        )


class NoTypeSpecifiedError(DAPSchemaParsingError):
    def __init__(self, table_name: str, prop_name: str) -> None:
        super().__init__(
            f"Cannot recognize type without `type` field in {table_name}.{prop_name}"
        )


class ReferenceError(DAPSchemaParsingError):
    def __init__(self, reference: str, table_name: str) -> None:
        super().__init__(
            f"References must start by referencing the root (#), Found {reference} in {table_name}"
        )


class CompositeKeyError(DAPSchemaParsingError):
    "Raised when the table schema has a composite primary key that comprises of multiple fields/columns."

    def __init__(self, table_name: str) -> None:
        super().__init__(f"Composite keys are not supported. Found in {table_name}")


class OneOfTypeSchemaError(DAPSchemaParsingError):
    def __init__(self, table_name: str) -> None:
        super().__init__(f"Only string is supported for oneOf types: {table_name}")


def create_table_definition(
    namespace: str, table_name: str, versioned_schema: VersionedSchema
) -> sqlalchemy.Table:
    """
    Creates SQLAlchemy table definition with the least step.

    :param namespace: Namespace that table belongs to.
    :param table_name: Identifier of the table.
    :param versioned_schema: Schema that the table conforms to.
    :returns: Table definition.
    :raises CompositeKeyError: The table has a composite primary key.
    """

    schema = typing.cast(Dict[str, JsonType], versioned_schema.schema["properties"])
    key_schema = typing.cast(Dict[str, JsonType], schema["key"])
    key_schema_props = typing.cast(Dict[str, JsonType], key_schema["properties"])

    if len(key_schema_props) != 1:
        raise CompositeKeyError(table_name)

    value_schema = typing.cast(Dict[str, JsonType], schema["value"])
    value_schema_props = typing.cast(Dict[str, JsonType], value_schema["properties"])
    columns: List[sqlalchemy.Column] = []

    required_keys = typing.cast(List[str], key_schema.get("required", []))
    for id_prop_name in key_schema_props.keys():
        id_schema = typing.cast(Schema, key_schema_props[id_prop_name])
        id_schema = resolve_ref(versioned_schema.schema, id_schema, table_name)

        column_type = match_type(id_schema, namespace, table_name, id_prop_name)

        columns.append(
            sqlalchemy.Column(
                id_prop_name,
                column_type,
                primary_key=True,
                nullable=(id_prop_name not in required_keys),
                comment=get_comment(id_schema),
            )
        )

    required_values = typing.cast(List[str], value_schema.get("required", []))
    for prop_name in value_schema_props.keys():
        prop_schema = typing.cast(Schema, value_schema_props[prop_name])
        prop_schema = resolve_ref(versioned_schema.schema, prop_schema, table_name)

        column_type = match_type(prop_schema, namespace, table_name, prop_name)

        columns.append(
            sqlalchemy.Column(
                prop_name,
                column_type,
                nullable=(prop_name not in required_values),
                comment=get_comment(prop_schema),
                default=get_default(prop_schema, namespace, table_name, prop_name),
            )
        )

    # create table model
    metadata = sqlalchemy.MetaData(schema=namespace)
    return sqlalchemy.Table(table_name, metadata, *columns)
