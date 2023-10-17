import dataclasses
import json
import typing
import uuid
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List

import typing_extensions
from cloudspec import CloudSpecParam


@dataclass
class ResourceProperty:
    type_: str = (
        None  # "string" | "boolean" | "integer" | "number" | "object" | "array" | null
    )
    description: str = None
    _ref: str = None  # $ref
    items: "ResourceProperty" = None  # used with properties of type "array"
    properties: Dict[
        str, "ResourceProperty"
    ] = None  # used with properties of type "object" for representing complex object
    enum: List[str] = None
    enum_descriptions: List[str] = None

    format: str = None  # "byte" | "double" | "float" | "int32" | "int64" | "uint32" | "uint64" | null
    # can be used to detail what type the string holds
    additional_properties: Dict[
        str, str
    ] = None  # can be used for more fine-grained typing?
    annotations: Dict[
        str, Any
    ] = None  # can be used to see if it is required for methods


@dataclass
class ResourceSchema:
    """Class representing GCP resource schema as returned by discovery API
    See: https://www.googleapis.com/discovery/v1/apis/compute/v1/rest
    """

    id_: str = None  # ref name
    description: str = None
    properties: Dict[str, ResourceProperty] = None


def parse_file(hub, path: str = "") -> Dict[str, ResourceSchema]:
    with open(path) as json_schema_file:
        schemas = json.load(json_schema_file)
    return hub.autogen.gcp.schema_parser.parse_json(schemas["schemas"])


def parse_json(hub, schemas: Dict[str, Any]) -> Dict[str, ResourceSchema]:
    schemas = {
        resource_name: _dataclass_from_dict(
            hub.autogen.gcp.schema_parser.sanitize_schema(resource_schema),
            ResourceSchema,
        )
        for (resource_name, resource_schema) in schemas.items()
    }
    return schemas


def parse_schemas(hub, schemas: Dict[str, ResourceSchema]) -> Dict[str, CloudSpecParam]:
    parsed_schemas = dict()
    for resource_name in schemas:
        hub.autogen.gcp.schema_parser.parse_schema(
            resource_name, schemas, parsed_schemas
        )
    return parsed_schemas


def parse_schema(
    hub,
    resource_name: str,
    schemas: Dict[str, ResourceSchema],
    parsed_schemas: Dict[str, CloudSpecParam],
):
    """Parses the schema for resource_name and all its dependencies, writes results to parsed_schemas"""
    resource_schema = schemas.get(resource_name)
    result = CloudSpecParam(
        name="unknown",
        required=False,
        target="kwargs",
        target_type="mapping",
        param_type="{}",
    )
    if resource_schema.description:
        result["doc"] = resource_schema.description

    member = {"name": resource_name}
    properties = resource_schema.properties
    member["params"] = {
        property_name: hub.autogen.gcp.schema_parser.parse_resource_prop(
            resource_prop, schemas, parsed_schemas, property_name
        )
        for (property_name, resource_prop) in properties.items()
    }
    result["member"] = member
    parsed_schemas[resource_name] = result
    return result


def parse_resource_prop(
    hub,
    resource_prop: ResourceProperty,
    schemas: Dict[str, ResourceSchema],
    parsed_schemas: Dict[str, CloudSpecParam],
    name: str = None,
) -> CloudSpecParam:
    if not name:
        name = "unknown"
    # name is known only in the wrapper context - enclosing type field name or top level parameter name
    result = CloudSpecParam(
        name=name, required=False, target="kwargs", target_type="mapping", doc=""
    )

    if resource_prop.description:
        result["doc"] = resource_prop.description

    if resource_prop.enum:
        enum_doc = hub.autogen.gcp.schema_parser.generate_enum_doc(
            resource_prop.enum, resource_prop.enum_descriptions
        )
        result["doc"] = hub.autogen.gcp.schema_parser.join_docs(result["doc"], enum_doc)

    if resource_prop.type_ and resource_prop.type_ not in {"object", "array"}:
        # TODO: see if we use different type names than returned by the API
        result["param_type"] = hub.autogen.gcp.schema_parser.convert_primitive_type(
            resource_prop.type_
        )

    elif resource_prop.type_ == "array":
        if resource_prop.items:
            parsed_member_cloudspec = hub.autogen.gcp.schema_parser.parse_resource_prop(
                resource_prop.items, schemas, parsed_schemas
            )
            if (
                parsed_member_cloudspec.param_type == "{}"
                and parsed_member_cloudspec.member
            ):
                result["param_type"] = "List[{}]"
                result["member"] = parsed_member_cloudspec.member
            else:
                result["param_type"] = f"List[{parsed_member_cloudspec.param_type}]"
                result["member"] = parsed_member_cloudspec.member
            # member_name = resource_prop.items._ref
            # if not member_name:
            #     member_name = "properties"
            # result["member"] = {
            #     "name": member_name,
            #     "params": parsed_member_cloudspec
            # }
        else:
            result["param_type"] = "List[Any]"

    elif resource_prop.type_ == "object" and resource_prop.properties:
        result["param_type"] = "{}"
        # TODO: cover cases where object is a ref (has additional_properties._ref)
        member = {"name": _generate_random_classname()}
        properties = resource_prop.properties
        member["params"] = {
            property_name: hub.autogen.gcp.schema_parser.parse_resource_prop(
                resource_prop, schemas, parsed_schemas, property_name
            )
            for (property_name, resource_prop) in properties.items()
        }
        result["member"] = member

    elif resource_prop.type_ == "object":
        result["param_type"] = "Dict[str, Any]"

    else:
        result["param_type"] = "Any"

    if resource_prop._ref:
        resource_name = resource_prop._ref
        if resource_name in parsed_schemas:
            parsed_schema = parsed_schemas[resource_name]
        else:
            parsed_schema = hub.autogen.gcp.schema_parser.parse_schema(
                resource_name, schemas, parsed_schemas
            )

        result["param_type"] = parsed_schema["param_type"]
        result["member"] = parsed_schema["member"]

        if parsed_schema.doc:
            result["doc"] = hub.autogen.gcp.schema_parser.join_docs(
                result["doc"], resource_name + ": " + parsed_schema.doc
            )

        # todo: add doc here

    return result


def convert_primitive_type(hub, gcp_type: str) -> str:
    if gcp_type == "boolean":
        return "bool"
    elif gcp_type == "string":
        return "str"
    elif gcp_type == "integer":
        return "int"
    elif gcp_type == "number":
        return "float"
    return "Any"


def generate_enum_doc(hub, enum_list: List[str], enum_descriptions: List[str]) -> str:
    if not enum_descriptions or len(enum_descriptions) != len(enum_list):
        #  descriptions are not as expected
        enum_descriptions = ["" for enum_value in enum_list]

    zipped = zip(enum_list, enum_descriptions)
    quoted_values = [
        f'"{enum_value}" - {enum_desc}' if enum_desc else f'"{enum_value}"'
        for (enum_value, enum_desc) in zipped
    ]
    return "Enum type. Allowed values:\n" + "\n".join(quoted_values)


def join_docs(hub, doc1: str, doc2: str) -> str:
    # removing empty docs
    docs = [doc for doc in [doc1, doc2] if doc]
    return "\n".join(docs)


def _dataclass_from_dict(d: Dict[str, Any], klass):
    field_types = {
        class_field.name: class_field.type for class_field in dataclasses.fields(klass)
    }
    raw_field_values = {
        dict_key: dict_value
        for (dict_key, dict_value) in d.items()
        if dict_key in field_types.keys()
    }
    return klass(
        **{
            field_name: _parse_raw_field_value(
                raw_field_value, field_types.get(field_name)
            )
            for (field_name, raw_field_value) in raw_field_values.items()
        }
    )


def _parse_raw_field_value(raw_field_value: Any, expected_type) -> Any:
    if dataclasses.is_dataclass(expected_type):
        return _dataclass_from_dict(raw_field_value, expected_type)
    if (
        expected_type == typing.ForwardRef("ResourceProperty")
        or expected_type == "ResourceProperty"
    ):
        return _dataclass_from_dict(raw_field_value, ResourceProperty)
    if (
        isinstance(raw_field_value, list)
        and typing_extensions.get_origin(expected_type) == list
    ):
        return [
            _parse_raw_field_value(
                list_value, typing_extensions.get_args(expected_type)[0]
            )
            for list_value in raw_field_value
        ]
    if (
        isinstance(raw_field_value, dict)
        and typing_extensions.get_origin(expected_type) == dict
    ):
        return {
            key: _parse_raw_field_value(
                value, typing_extensions.get_args(expected_type)[1]
            )
            for (key, value) in raw_field_value.items()
        }
    return raw_field_value


def sanitize_schema(hub, schema: Any) -> Any:
    if isinstance(schema, dict):
        return {
            hub.autogen.gcp.schema_parser.sanitize_key(
                key
            ): hub.autogen.gcp.schema_parser.sanitize_schema(value)
            for (key, value) in schema.items()
        }
    if isinstance(schema, list):
        return [hub.autogen.gcp.schema_parser.sanitize_schema(item) for item in schema]
    return schema


def sanitize_key(hub, key: str) -> str:
    return hub.tool.gcp.case.unclash(hub.tool.gcp.case.snake(key))


def _generate_random_classname() -> str:
    return "Class" + str(uuid.uuid4()).replace("-", "")
