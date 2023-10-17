"""Utilities for Google Cloud Platform APIs.

Copyright (c) 2021-2022 VMware, Inc.
SPDX-License-Identifier: Apache-2.0
"""
import copy
import json
import logging
import re
from copy import deepcopy
from typing import Any
from typing import Dict
from typing import List
from typing import Set

import dict_tools.differ as differ
from deepdiff import DeepDiff
from dict_tools.data import NamespaceDict

# Import plugin helpers

log = logging.getLogger(__name__)


def _is_empty(o) -> bool:
    return not isinstance(o, bool) and not o


def _is_within_dict(parent, o, ignore: set):
    """Determine of an object is within a parent dict object.

    :param parent: The object in which o hopefully exists.
    :param o: The object to find in parent.
    :param ignore: A set of keys to ignore in parent.
    return: True if o is within parent somewhere. False otherwise.
    """
    ret = True
    for k, v in o.items():
        if k in ignore:
            break
        elif k not in parent:
            # TODO: Handle pure default value cases.
            # Need to handle cases where the state spec provides a key
            # the value of which containes purely default values. Google APIs
            # responses do not present keys filled with default values.
            if not _is_empty(o[k]):
                ret = False
                break
        elif not _is_empty(o[k]) and _is_empty(parent[k]):
            ret = False
            break
        elif not _is_within(parent[k], v, ignore):
            ret = False
            break
    return ret


def _is_within_list(parent, o, ignore: set):
    """Determine of an object is within a parent list object.

    :param parent: The object in which o hopefully exists.
    :param o: The object to find in parent.
    :param ignore: A set of keys to ignore in parent.
    return: True if o is within parent somewhere. False otherwise.
    """
    ret = True
    plen = len(parent)

    if len(o) > len(parent):
        ret = False
    else:
        for oidx in range(len(o)):
            inner_ret = False
            for pidx in range(plen):
                if _is_within(parent[pidx], o[oidx], ignore):
                    inner_ret = True
                    break
            if not inner_ret:
                ret = inner_ret
                break

    return ret


def _is_within_set(parent, o, ignore: set):
    """Determine of an object is within a parent set object.

    :param parent: The object in which o hopefully exists.
    :param o: The object to find in parent.
    :param ignore: A set of keys to ignore in parent.
    return: True if o is within parent somewhere. False otherwise.
    """
    return _is_within_list(list(parent), list(o), ignore)


def _is_within(parent, o, ignore: set):
    """Determine of an object is within a parent object.

    :param parent: The object in which o hopefully exists.
    :param o: The object to find in parent.
    :param ignore: A set of keys to ignore in parent.
    return: True if o is within parent somewhere. False otherwise.
    """
    if not isinstance(parent, type(o)):
        return False
    elif isinstance(o, dict):
        return _is_within_dict(parent, o, ignore)
    elif isinstance(o, list):
        return _is_within_list(parent, o, ignore)
    elif isinstance(o, set):
        return _is_within_set(parent, o, ignore)
    elif isinstance(o, tuple):
        return _is_within_list(parent, o, ignore)
    elif isinstance(o, str):
        return o in parent
    else:
        return parent == o


def is_within(hub, parent, o, ignore: set = {}):
    """Returns True if the object (o) is contained within parent (top level) object.

    :param hub: The redistributed pop central hub. This is required in
    Idem, so while not used, must appear.
    :param parent: The object to check if contains o.
    :param o: An object to check if is within the parent object.
    :return: False if parent and o are different types or do not compare,
    otherwise True.

    For example:

    The subset:

    { name: "my_object" }

    exists within

    { something_else: "some other thing", name: "my_object" },
    """
    return _is_within(parent, o, ignore)


# TODO: Cover the merge logic with tests
def _merge_dicts(target: Dict, source: Dict) -> Dict:
    if not source:
        return target
    new_target: Dict = {}
    for key in source:
        if key not in target or not isinstance(target[key], dict):
            new_target[key] = deepcopy(source[key])
        else:
            new_target[key] = _merge_dicts(target[key], source[key])
    return new_target


def merge_dicts(hub, target: dict, source: dict) -> dict:
    """Returns the dict resulting from overwriting values within a source dict into a target dict, recursively.

    All values within a key from the source
    will overwrite the same within the target. For example, consider the
    following merged result:

       source = { 'text': ["this", "is", "my_object"] }
       target = { 'text': ["not', "this" "time"], 'place': "elsewhere" }

       merged = { 'text': ["this", "is", "my_object" ], 'place': "elsewhere" }

    :param hub: The redistributed pop central hub. This is required in
    Idem, so while not used, must appear.
    :param target: The dict into which to merge the source.
    :param source: The dict from which to merge into the target.
    :return: dict as merged.
    """
    return _merge_dicts(target, source)


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """
    This method enables state specific implementation of is_pending logic,
    based on resource specific attribute(s).
    Usage 'idem state <sls-file> --reconciler=basic', where the reconciler attribute
    can be missed.

    :param hub: The Hub into which the resolved callable will get placed.
    :param ret: The returned dictionary of the last run.
    :param state: The name of the state.
    :param pending_kwargs: (dict, Optional) May include 'ctx' and 'reruns_wo_change_count'.

    :return: True | False
    """
    if not ret:
        return False

    if ret.get("rerun_data") and ret["rerun_data"].get("has_error", False):
        return False

    if ret.get("rerun_data"):
        return True

    if ret["result"]:
        return False

    return pending_kwargs and pending_kwargs.get("reruns_wo_change_count", 0) < 4


def compare_states(
    hub,
    # actual
    old_state: Dict,
    # expected
    plan_state: Dict,
    resource_type: str = None,
    additional_exclude_paths: List[str] = None,
) -> Dict:
    exclude_paths = (
        hub.tool.gcp.utils.format_exclude_paths(additional_exclude_paths)
        if additional_exclude_paths
        else []
    )

    old_state = hub.tool.gcp.sanitizers.sanitize_resource_urls(old_state)
    plan_state = hub.tool.gcp.sanitizers.sanitize_resource_urls(plan_state)
    if (old_state is None or plan_state is None) and old_state != plan_state:
        return DeepDiff(
            old_state,
            plan_state,
            exclude_regex_paths=exclude_paths,
            ignore_type_in_groups=[(NamespaceDict, dict)],
        )

    for key in old_state.keys():
        if key not in plan_state:
            exclude_paths.append(f"root['{key}']")

    if resource_type:
        exclude_paths.extend(
            hub.tool.gcp.utils.get_deep_diff_exclude_paths(resource_type)
        )

    changes = DeepDiff(
        old_state,
        plan_state,
        exclude_regex_paths=exclude_paths,
        ignore_type_in_groups=[(NamespaceDict, dict)],
    )

    hub.tool.gcp.utils.filter_diff(changes, plan_state)
    # If an item is in old_state but not in plan_state, i.e. changes.get("dictionary_item_removed") is not None,
    # we can ignore this change

    # TODO: changes.get("dictionary_item_removed") also includes nested items, which means deleted nested items
    #  are ignored. Ignore only root items and read-only nested items
    # type_changes can occur when a value was previously None (NoneType) and then a value was specified

    relevant_dictionary_item_removed = (
        hub.tool.gcp.utils.get_relevant_dictionary_item_removed(
            resource_type, changes.get("dictionary_item_removed")
        )
    )

    relevant_changes = (
        set(changes.get("dictionary_item_added") or set())
        | set(relevant_dictionary_item_removed or set())
        | set(changes.get("iterable_item_added") or set())
        | set(changes.get("iterable_item_removed") or set())
        | set(changes.get("values_changed") or set())
        | set(changes.get("type_changes") or set())
    )

    if not relevant_changes:
        return {}

    changes["relevant_changes"] = relevant_changes
    return changes


def get_relevant_dictionary_item_removed(
    hub, resource_type: str, dictionary_items_removed: Set
) -> Set:
    relevant_items_removed = set()
    if not dictionary_items_removed:
        return relevant_items_removed

    defined_relevant_dict_items_removed = (
        hub.tool.gcp.resource_prop_utils.get_relevant_dict_items_removed(resource_type)
    )

    # Example:
    # Relevant items removed are the dictionary items of compute.instance property labels
    # Property -> [compute.instance] -> labels.dictKeysPlaceholder
    # As dict label keys are user defined, we mark them with the dictKeysPlaceholder in properties.yaml
    # Every property from properties.yaml is converted from camel to snake case -> dict_keys_placeholder
    # Regex -> "^root\\['labels'\\]\\['\\w+'\\]$"
    # Match -> "root['labels']['label_key_example']"
    defined_relevant_dict_items_removed_regexes = [
        _build_deep_diff_property_regex_pattern(x)
        for x in defined_relevant_dict_items_removed
    ]

    for item in dictionary_items_removed:
        # check if the removed item matches with one of the properties which removal is relevant
        for regex in defined_relevant_dict_items_removed_regexes:
            if regex.match(item):
                relevant_items_removed.add(item)

    return relevant_items_removed


def _build_deep_diff_property_regex_pattern(source: str):
    # mark the regex beginning
    result = "^root"

    properties = source.split(".")
    for prop in properties:
        if "[]" in prop:
            prop_name = prop.replace("[]", "")
            result += f"\\['{prop_name}'\\]\\[\\d+\\]"
        if "dict_keys_placeholder" == prop:
            prop_name = prop.replace("dict_keys_placeholder", "\\['.+'\\]")
            result += prop_name
        else:
            result += f"\\['{prop}'\\]"

    # mark the regex ending
    result += "$"
    return re.compile(result)


def _clean_state_from_excluded_paths(state, exclude_paths):
    cleaned_state = state if state else dict()
    for exclude_path in exclude_paths:
        path_elements = exclude_path.split(".")
        _pop_nested_key_from_dict(cleaned_state, path_elements)
    return cleaned_state


def _pop_nested_key_from_dict(state, key_path):
    if not key_path:
        return

    if not state or not isinstance(state, dict):
        return

    root_path_segment = key_path[0]

    if len(key_path) == 1:
        state.pop(root_path_segment, None)
        return

    if root_path_segment.endswith("[]"):
        root_path_segment = root_path_segment[:-2]
        lst = state.get(root_path_segment, [])
        if not isinstance(lst, list):
            return
        for element in lst:
            _pop_nested_key_from_dict(element, key_path[1:])
    else:
        nested_obj = state.get(root_path_segment, {})
        _pop_nested_key_from_dict(nested_obj, key_path[1:])


def compare_changes(
    hub,
    old_state: NamespaceDict,
    new_state: NamespaceDict,
    resource_type: str = None,
) -> Dict:
    exclude_paths = (
        hub.tool.gcp.resource_prop_utils.get_exclude_paths(resource_type)
        if resource_type
        else []
    )
    cleaned_old_state = _clean_state_from_excluded_paths(
        copy.deepcopy(old_state), exclude_paths
    )
    cleaned_new_state = _clean_state_from_excluded_paths(
        copy.deepcopy(new_state), exclude_paths
    )
    return differ.deep_diff(cleaned_old_state, cleaned_new_state)


def get_plan_state_value_from_deep_diff_path(hub, deep_diff_path: str, plan_state):
    result = plan_state
    # remove root prefix
    deep_diff_path = deep_diff_path[4:]
    while deep_diff_path:
        if deep_diff_path.startswith("['"):
            deep_diff_path = deep_diff_path[2:]
            end_index = deep_diff_path.find("']")
            path_segment = deep_diff_path[:end_index]
            result = result.get(path_segment)
            deep_diff_path = deep_diff_path[end_index + 2 :]
        elif deep_diff_path.startswith("["):
            #
            deep_diff_path = deep_diff_path[1:]
            end_index = deep_diff_path.find("]")
            index_string = deep_diff_path[:end_index]
            if index_string.isdecimal():
                index = int(index_string)
                result = result[index] if index < len(result) else None
            deep_diff_path = deep_diff_path[end_index + 1 :]
        if not result:
            return result

    return result


def get_deep_diff_exclude_paths(hub, resource_type: str):
    paths = hub.tool.gcp.resource_prop_utils.get_exclude_paths(resource_type)
    return hub.tool.gcp.utils.format_exclude_paths(paths)


def format_exclude_paths(hub, paths):
    exclude_paths = []
    for path in paths:
        s = "root"
        for part in path.split("."):
            if part.endswith("[]"):
                s += f"\\['{part[:-2]}'\\]\\[\\d+\\]"
            else:
                s += f"\\['{part}'\\]"
        exclude_paths.append(s)
    return exclude_paths


def filter_diff(hub, changes, plan_state):
    # filter out added empty list values - assume they're the default ones
    added_items = changes.get("dictionary_item_added")
    if added_items:
        filtered_added_items = copy.copy(added_items)
        for added_item in added_items:
            value = hub.tool.gcp.utils.get_plan_state_value_from_deep_diff_path(
                added_item, plan_state
            )
            if value == []:
                filtered_added_items.remove(added_item)
        changes["dictionary_item_added"] = filtered_added_items


def get_project_from_account(hub, ctx: dict, project: str = None) -> str:
    """If project is explicitly passed by the user, this project will be returned.
    If project is empty, this method will return gcp account default project
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param project: A string explicitly passed by the user.
    :return: the correct project
    """
    if not project:
        project = ctx.get("acct", {}).get("project_id")
    if not project:
        hub.log.warning("Could not find project info from account")
    return project


# TODO: Enhance this method to work for multi dictionary layers as opposed to now working with only the top one.
def create_dict_body_on_top_of_old(
    hub, old: Dict[str, Any], new: Dict[str, Any]
) -> Dict[str, Any]:
    result = copy.copy(old)
    for key, value in new.items():
        result[key] = value

    return result


# zonal absent method signature
async def zonal_absent(
    hub,
    ctx,
    name: str,
    project: str = None,
    zone: str = None,
    resource_id: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""Deletes the resource.

    Args:
        name(str, Optional):
            An Idem name of the resource.

        project(str, Optional):
            Project ID for this request.

        zone:(str, Optional):
            The name of the zone for this request.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]
    """
    # the method is handled via the recursive_contracts->call_absent
    raise NotImplementedError


# global absent method signature
async def regional_absent(
    hub,
    ctx,
    name: str,
    project: str = None,
    region: str = None,
    resource_id: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""Deletes the resource.

    Args:
        name(str, Optional):
            An Idem name of the resource.

        project(str, Optional):
            Project ID for this request.

        region(str, Optional):
            The name of the region for this request.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]
    """
    # the method is handled via the recursive_contracts->call_absent
    raise NotImplementedError


# global absent method signature
async def global_absent(
    hub,
    ctx,
    name: str,
    project: str = None,
    resource_id: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""Deletes the resource.

    Args:
        name(str, Optional):
            An Idem name of the resource.

        project(str):
            Project ID for this request.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]
    """
    # the method is handled via the recursive_contracts->call_absent
    raise NotImplementedError


def get_esm_tagged_data(hub, data: Dict, resource_type: str = None):
    ret = None
    found: bool = False
    for key, value in data.items():
        if "_|-" in key:
            if resource_type:
                res_type, _, _, _ = key.split("_|-", maxsplit=3)
                if res_type != resource_type:
                    continue
            if found:
                raise ValueError("Duplicate matching tags found!")
            ret = value
            found = True

    if not found:
        raise ValueError("No matching tag found!")

    return ret


def convert_to_regular_dict(hub, input_dict: NamespaceDict) -> dict:
    return json.loads(hub.output.json.display(input_dict))
