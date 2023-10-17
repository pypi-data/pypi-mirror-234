# TODO: How to handle corner cases like abcXYZ ?
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Set


# TODO: make this work with the JSON schemas so that we can handles cases such as abcXYZ
def convert_raw_resource_to_present(
    hub,
    raw_resource: Dict[str, Any],
    resource_type_name: str = None,
    exclude_properties_from_transformation: List[str] = None,
) -> Dict[str, Any]:
    if resource_type_name and exclude_properties_from_transformation is None:
        exclude_properties_from_transformation = (
            hub.tool.gcp.resource_prop_utils.get_exclude_keys_from_transformation(
                raw_resource, resource_type_name, is_raw_resource=True
            )
        )
    return _convert_resource(
        raw_resource,
        hub.tool.gcp.case.sanitize_key,
        exclude_properties_from_transformation,
    )


def convert_present_resource_to_raw(
    hub,
    present_resource: Dict[str, Any],
    resource_type_name: str = None,
    exclude_properties_from_transformation: List[str] = None,
    present_to_raw_manual_mappings: Dict[str, str] = None,
) -> Dict[str, Any]:
    if resource_type_name and exclude_properties_from_transformation is None:
        exclude_properties_from_transformation = (
            hub.tool.gcp.resource_prop_utils.get_exclude_keys_from_transformation(
                present_resource, resource_type_name, is_raw_resource=False
            )
        )
    return _convert_resource(
        present_resource,
        hub.tool.gcp.case.camel,
        exclude_properties_from_transformation,
        manual_mappings=present_to_raw_manual_mappings,
    )


def _convert_resource(
    resource,
    key_transformer: Callable[[Any], Any],
    exclude_properties_from_transformation: List[str] = None,
    path_prefix: str = "",
    manual_mappings: Dict[str, str] = None,
):
    if resource is None:
        return None

    manual_mappings = manual_mappings or {}

    if exclude_properties_from_transformation is None:
        exclude_properties_from_transformation = []

    if isinstance(resource, list):
        return list(
            _convert_resource(
                v,
                key_transformer,
                exclude_properties_from_transformation,
                path_prefix,
                manual_mappings,
            )
            for v in resource
        )
    elif isinstance(resource, set):
        return {
            _convert_resource(
                v,
                key_transformer,
                exclude_properties_from_transformation,
                path_prefix,
                manual_mappings,
            )
            for v in resource
        }
    elif isinstance(resource, dict):
        result = {}
        for k, v in resource.items():
            if k in exclude_properties_from_transformation:
                key = k
            elif f"{path_prefix}{k}" in manual_mappings:
                key = manual_mappings[f"{path_prefix}{k}"]
            else:
                key = key_transformer(k)
            value = _convert_resource(
                v,
                key_transformer,
                exclude_properties_from_transformation,
                f"{path_prefix}{k}.",
                manual_mappings,
            )
            result[key] = value
        return result
    else:
        return resource


def convert_raw_properties_to_present(hub, raw_properties: Set) -> Set:
    if not raw_properties:
        return set()

    properties_translated = set()

    for value in raw_properties:
        properties_translated.add(hub.tool.gcp.case.sanitize_key(value))

    return properties_translated


def convert_present_properties_to_raw(hub, present_properties: Set) -> Set:
    if not present_properties:
        return set()

    properties_translated = set()

    for value in present_properties:
        properties_translated.add(hub.tool.gcp.case.camel(value))

    return properties_translated
