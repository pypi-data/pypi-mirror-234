import re
from typing import Any
from typing import Dict
from typing import List
from typing import Set

import yaml
from deepdiff import DeepDiff
from importlib_resources import files


def __init__(hub):
    file_text = (
        files("idem_gcp.resources")
        .joinpath("properties.yaml")
        .read_text(encoding="utf-8")
    )

    # TODO: Maybe convert the properties names in hub.tool.gcp.RESOURCE_PROPS
    #  to snake case here so that we do not have to do conversion
    #  very often anywhere these snake case properties names are needed.
    #  Check if hub.tool.gcp.RESOURCE_PROPS are always convert to snake case

    hub.tool.gcp.RESOURCE_PROPS = yaml.safe_load(file_text)


def get_create_properties(
    hub, resource_type: str, convert_to_present: bool = True
) -> Set:
    resource_methods_properties = hub.tool.gcp.RESOURCE_PROPS[resource_type]
    raw_props = set(
        resource_methods_properties.get("insert", {})
        or resource_methods_properties.get("create", {})
    )
    if raw_props and convert_to_present:
        return hub.tool.gcp.conversion_utils.convert_raw_properties_to_present(
            raw_props
        )
    return raw_props


def get_update_properties(
    hub, resource_type: str, convert_to_present: bool = True
) -> Set:
    raw_props = set(hub.tool.gcp.RESOURCE_PROPS[resource_type].get("update", {}))
    if raw_props and convert_to_present:
        return hub.tool.gcp.conversion_utils.convert_raw_properties_to_present(
            raw_props
        )
    return raw_props


def get_fields_of_enum_type(
    hub, resource_type: str, convert_to_present: bool = True
) -> Set:
    raw_props = set(
        hub.tool.gcp.RESOURCE_PROPS[resource_type].get("fields_enum_type", {})
    )
    if convert_to_present:
        return hub.tool.gcp.conversion_utils.convert_raw_properties_to_present(
            raw_props
        )
    return raw_props


def get_non_updatable_properties(hub, resource_type: str) -> Set:
    raw_non_updatable_properties = set()

    raw_non_updatable_properties.update(
        hub.tool.gcp.RESOURCE_PROPS[resource_type].get(
            "nested_non_updatable_properties", []
        )
    )

    raw_non_updatable_properties.update(
        hub.tool.gcp.resource_prop_utils.get_create_properties(resource_type)
        - hub.tool.gcp.resource_prop_utils.get_update_properties(resource_type)
    )

    raw_non_updatable_properties.update(
        hub.tool.gcp.resource_prop_utils.get_readonly_return_props(resource_type)
    )

    non_updatable_properties = set(
        hub.tool.gcp.conversion_utils.convert_raw_properties_to_present(
            raw_non_updatable_properties
        )
    )

    return non_updatable_properties


def get_changed_non_updatable_properties(
    hub, resource_type: str, changes: DeepDiff
) -> Set:
    if not changes:
        return set()

    non_updatable_properties = (
        hub.tool.gcp.resource_prop_utils.get_non_updatable_properties(resource_type)
    )

    changed_non_updatable_properties = set()

    for changed_property_full_path in changes.get("relevant_changes", {}):
        # This formats changed_property_full_path from e.g. "root['network_interfaces'][0]['alias_ip_ranges']"
        # to "network_interfaces[].alias_ip_ranges"
        changed_property_path_elements = re.findall(
            r"(?<=\[).*?(?=\])", changed_property_full_path
        )
        formatted_path_elements = []
        for i in range(len(changed_property_path_elements)):
            if changed_property_path_elements[i].isdigit():
                formatted_path_elements.append("[]")
            else:
                if i > 0:
                    formatted_path_elements.append(".")
                formatted_path_elements.append(
                    changed_property_path_elements[i].strip("'")
                )
        formatted_property_path = "".join(formatted_path_elements)
        if formatted_property_path in non_updatable_properties:
            changed_non_updatable_properties.add(formatted_property_path)

    return changed_non_updatable_properties


def get_present_properties(hub, resource_type: str) -> Set:
    return (
        hub.tool.gcp.resource_prop_utils.get_create_properties(resource_type, False)
        .union(
            hub.tool.gcp.resource_prop_utils.get_update_properties(resource_type, False)
        )
        .union(
            hub.tool.gcp.resource_prop_utils.get_fields_of_enum_type(
                resource_type, False
            )
        )
        .union(
            hub.tool.gcp.resource_prop_utils.get_readonly_return_props(
                resource_type, False
            )
        )
    )


def get_exclude_paths(hub, resource_type: str) -> Set:
    raw_props_names = hub.tool.gcp.RESOURCE_PROPS[resource_type].get(
        "exclude_paths", []
    )
    return set(
        hub.tool.gcp.conversion_utils.convert_raw_properties_to_present(raw_props_names)
    )


def get_exclude_properties_from_transformation(
    hub, resource_type: str, convert_to_present: bool
) -> Set:
    resource_methods_properties = hub.tool.gcp.RESOURCE_PROPS[resource_type]
    raw_props = set(
        resource_methods_properties.get("exclude_properties_from_transformation", {})
    )
    if raw_props and convert_to_present:
        return hub.tool.gcp.conversion_utils.convert_raw_properties_to_present(
            raw_props
        )
    return raw_props


def get_exclude_keys_from_transformation(
    hub, resource_body: Dict[str, Any], resource_type: str, is_raw_resource: bool
) -> List[str]:
    # Get the properties whose keys should be excluded from transformation
    exclude_properties_from_transformation = (
        hub.tool.gcp.resource_prop_utils.get_exclude_properties_from_transformation(
            resource_type, convert_to_present=(not is_raw_resource)
        )
    )

    exclude_keys_from_transformation = []
    _populate_list_with_keys_from_specified_dict_properties(
        resource_body,
        exclude_properties_from_transformation,
        exclude_keys_from_transformation,
    )

    return exclude_keys_from_transformation


def _populate_list_with_keys_from_specified_dict_properties(
    resource,
    properties: List[str],
    key_list: List[str],
    path_prefix: str = "",
) -> List[str]:
    if key_list is None:
        return

    if isinstance(resource, list) or isinstance(resource, set):
        for item in resource:
            _populate_list_with_keys_from_specified_dict_properties(
                item, properties, key_list, path_prefix
            )
    elif isinstance(resource, dict):
        for k, v in resource.items():
            if k in properties:
                if resource.get(k) and isinstance(resource[k], dict):
                    key_list += list(resource[k].keys())
            else:
                _populate_list_with_keys_from_specified_dict_properties(
                    v, properties, key_list, f"{path_prefix}{k}."
                )
    return


def extract_resource_id(hub, input_props: Dict, resource_type: str) -> Dict:
    if "selfLink" in input_props:
        return hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            input_props.get("selfLink"), resource_type
        )

    if "resource_id" in hub.tool.gcp.RESOURCE_PROPS[resource_type]:
        resource_id_fields = hub.tool.gcp.RESOURCE_PROPS[resource_type]["resource_id"]
        for resource_id_field in resource_id_fields:
            if resource_id_field in input_props:
                return input_props[resource_id_field]


def get_resource_paths(hub, resource_type: str) -> List[str]:
    resource_path = resource_type.split(".")
    hub_ref = hub.metadata.gcp
    for resource_path_segment in resource_path:
        hub_ref = hub_ref[resource_path_segment]

    result = hub_ref["PATH"]
    return result if isinstance(result, list) else [result]


def get_elements_from_resource_id(hub, resource_type: str, resource_id: str) -> Dict:
    resource_paths = hub.tool.gcp.resource_prop_utils.get_resource_paths(resource_type)

    result = None
    for path in resource_paths:
        r = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id_and_path(
            resource_type, resource_id, path
        )
        if r:
            if result:
                msg = f"Resource ID {resource_id} matches multiple resource paths of {resource_type}"
                hub.log.error(msg)
                return {}
            result = r

    if not result:
        comment = hub.tool.gcp.comment_utils.ill_formed_resource_id_comment(
            resource_type, resource_id, resource_paths
        )
        raise ValueError(comment)

    return result


def get_elements_from_resource_id_and_path(
    hub, resource_type: str, resource_id: str, resource_path: str
) -> Dict:
    src = resource_path.split("/")
    act = resource_id.split("/")
    result = {}

    if len(act) < len(src):
        return {}

    idx = -1
    for s in reversed(src):
        val = act[idx]
        if s.startswith("{") and s.endswith("}"):
            key = s[1:-1]
            result[key] = val
        elif val != s:
            return {}
        idx -= 1

    return result


def parse_link_to_resource_id_and_path(
    hub, link, resource_type: str, resource_path: str
) -> str:
    result = resource_path
    src = result.split("/")
    act = link.split("/")

    if len(act) < len(src):
        return None

    idx = -1
    for s in reversed(src):
        val = act[idx]
        if s.startswith("{") and s.endswith("}"):
            result = result.replace(s, val)
        elif val != s:
            return None
        idx -= 1

    return result


def parse_link_to_resource_id(
    hub, link, resource_type: str, log_warnings: bool = True
) -> str:
    resource_paths = hub.tool.gcp.resource_prop_utils.get_resource_paths(resource_type)
    result = None
    for path in resource_paths:
        r = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id_and_path(
            link, resource_type, path
        )
        if r:
            if result:
                msg = f"Link {link} matches multiple resource paths of {resource_type}"
                hub.log.error(msg)
                return None
            result = r

    if not result:
        if log_warnings:
            msg = f"Link {link} matches no resource paths of {resource_type}"
            hub.log.warning(msg)
        return None

    return result


def construct_resource_id(hub, resource_type: str, input_props: Dict[str, Any]) -> str:
    if input_props is not None and input_props.get("name") is not None:
        # handle case where "name" contains full resource id
        name = input_props.get("name")
        try:
            if (
                hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                    name, resource_type, log_warnings=False
                )
                is not None
            ):
                return name
        except ValueError:
            pass

    filtered_without_none_properties = (
        {k: v for k, v in input_props.items() if v is not None}
        if input_props is not None
        else {}
    )
    resource_paths: List[str] = hub.tool.gcp.resource_prop_utils.get_resource_paths(
        resource_type
    )
    for path in resource_paths:
        try:
            r = path.format(**filtered_without_none_properties)
            if r.find("{") == -1 and r.find("}") == -1:
                # fully matched
                return r
        except KeyError:
            ...

    msg = f"Could not construct resource ID because no resource paths of {resource_type} match the input arguments."
    hub.log.warning(msg)
    return None


def parse_link_to_zone(hub, link: str) -> str:
    return link.split("/")[-1]


def get_path_parameters_for_path(hub, resource_path: str) -> Set[str]:
    src = resource_path.split("/")
    result = set()

    for s in src:
        if s.startswith("{") and s.endswith("}"):
            result.add(s[1:-1])

    return result


def get_path_parameters(hub, resource_type: str, resource: str) -> Set[str]:
    resource_paths = hub.tool.gcp.resource_prop_utils.get_resource_paths(resource_type)
    all_parameters = []
    for path in resource_paths:
        r = hub.tool.gcp.resource_prop_utils.get_path_parameters_for_path(path)
        if r:
            all_parameters.append(r)

    # Try to find best-matching path
    result = None
    for parameters in all_parameters:
        missing = {p for p in parameters if p not in resource}
        if not missing:
            if result:
                msg = f"Resource {resource} matches multiple resource paths of {resource_type}"
                hub.log.error(msg)
                return set()

            result = parameters

    if not result:
        msg = f"Resource {resource} matches no resource paths of {resource_type}"
        hub.log.warning(msg)
        return set()

    return result


def get_path_parameters_combined(hub, resource_type: str, resource: str) -> Set[str]:
    resource_paths = hub.tool.gcp.resource_prop_utils.get_resource_paths(resource_type)
    all_parameters = []
    for path in resource_paths:
        r = hub.tool.gcp.resource_prop_utils.get_path_parameters_for_path(path)
        if r:
            all_parameters.append(r)

    result = set()
    for parameters in all_parameters:
        result = result.union(parameters)

    return result


def format_path_params(hub, resource, resource_type):
    path_params = hub.tool.gcp.resource_prop_utils.get_path_parameters_combined(
        resource_type, resource
    )
    for path_el in path_params:
        if resource.get(path_el):
            resource[path_el] = resource[path_el].split("/")[-1]


# TODO: Remove this logic once we have all the nested properties defined for a method
def are_properties_allowed_for_update(hub, resource_type, request_body):
    can_update = True
    if resource_type == "compute.instance":
        for disk in request_body.get("disks" or {}):
            if disk.get("initialize_params"):
                can_update = False

    return can_update


def resource_type_matches(hub, resource_id: str, resource_type: str) -> bool:
    resource_paths = hub.tool.gcp.resource_prop_utils.get_resource_paths(resource_type)
    result = False
    for path in resource_paths:
        r = hub.tool.gcp.resource_prop_utils.resource_type_matches_for_path(
            resource_id, path
        )
        if r:
            if result:
                msg = f"Resource ID {resource_id} matches multiple resource paths of {resource_type}"
                hub.log.error(msg)
                return False
            result = True

    return result


def resource_type_matches_for_path(hub, resource_id: str, resource_path: str) -> bool:
    rpath = resource_path.split("/")
    rid = resource_id.split("/")

    if len(rid) < len(rpath):
        return False

    idx = -1
    for s in reversed(rpath):
        if not (s.startswith("{") and s.endswith("}")) and rid[idx] != s:
            return False
        idx -= 1

    return True


def get_manual_mappings(hub, resource_type: str) -> Dict[str, str]:
    resource_methods_properties = hub.tool.gcp.RESOURCE_PROPS[resource_type]
    manual_mappings = resource_methods_properties.get("manual_mapping", {})
    return manual_mappings


def get_missing_property_assumed_values(hub, resource_type: str) -> Dict[str, Any]:
    resource_properties = hub.tool.gcp.RESOURCE_PROPS.get(resource_type, {})
    return resource_properties.get("missing_property_assumed_value", {})


def populate_resource_with_assumed_values(
    hub, resource, resource_type, convert_to_present: bool = False
):
    assumed_values = (
        hub.tool.gcp.resource_prop_utils.get_missing_property_assumed_values(
            resource_type
        )
    )

    if convert_to_present:
        assumed_values = hub.tool.gcp.conversion_utils.convert_raw_resource_to_present(
            assumed_values, resource_type
        )

    for missing_key, assumed_value in assumed_values.items():
        if missing_key not in resource:
            resource[missing_key] = assumed_value


def get_readonly_return_props(
    hub, resource_type: str, convert_to_present: bool = True
) -> Set[str]:
    resource_properties = hub.tool.gcp.RESOURCE_PROPS.get(resource_type, {})

    raw_props = set(resource_properties.get("readonly_return_props", {}))

    if raw_props and convert_to_present:
        return hub.tool.gcp.conversion_utils.convert_raw_properties_to_present(
            raw_props
        )

    return raw_props


def properties_mismatch_resource_id(
    hub, service_resource_type, resource_id, state_properties
) -> bool:
    constructed_resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
        service_resource_type, state_properties
    )
    # This check is needed if properties or resource_id are not supplied
    if not constructed_resource_id or not resource_id:
        return False
    if resource_id != constructed_resource_id:
        return True
    return False


# TODO: Figure out a generic way to get the native resource path
def get_service_resource_type(hub, state_resource_path: str) -> str:
    service_resource_path = state_resource_path.replace("gcp.", "")
    if "cloudkms" not in service_resource_path:
        return service_resource_path

    cloudkms_native_resource_paths_dict = {
        "cloudkms.location": "cloudkms.projects.locations",
        "cloudkms.key_ring": "cloudkms.projects.locations.key_rings",
        "cloudkms.import_job": "cloudkms.projects.locations.key_rings.import_jobs",
        "cloudkms.crypto_key": "cloudkms.projects.locations.key_rings.crypto_keys",
        "cloudkms.crypto_key_version": "cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions",
    }

    return cloudkms_native_resource_paths_dict[service_resource_path]


def get_relevant_dict_items_removed(
    hub, resource_type: str, convert_to_present: bool = True
) -> List[str]:
    resource_methods_properties = hub.tool.gcp.RESOURCE_PROPS.get(resource_type, {})
    raw_props = set(resource_methods_properties.get("relevant_dict_items_removed", {}))
    if raw_props and convert_to_present:
        return hub.tool.gcp.conversion_utils.convert_raw_properties_to_present(
            raw_props
        )

    return raw_props
