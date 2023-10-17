"""State module for managing InstanceGroups."""

__contracts__ = ["resource"]

from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from idem_gcp.tool.gcp.state_operation_utils import StateOperations
from idem_gcp.tool.gcp.utils import zonal_absent

# prevent commit hook from removing the import
absent = zonal_absent

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    zone: str = None,
    project: str = None,
    description: str = None,
    fingerprint: str = None,
    subnetwork: str = None,
    network: str = None,
    named_ports: List[
        make_dataclass(
            "NamedPort",
            [("name", str, field(default=None)), ("port", int, field(default=None))],
        )
    ] = None,
    request_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Create or update an instance group.

    Creates an instance group in the specified project using the parameters that are included in the request.

    Args:
        name(str):
            An Idem name of the resource.

        description(str, Optional):
            An optional description of this resource. Provide this property when you create the resource. Defaults to None.

        zone(str):
            The name of the zone where the instance group is located.

        fingerprint(str, Optional):
            The fingerprint of the named ports. The system uses this fingerprint to detect conflicts when multiple users change the named ports concurrently. Defaults to None.

        network(str, Optional):
            The URL of the network to which all instances in the instance group belong. If your instance has multiple network interfaces, then the network and subnetwork fields only refer to the network and subnet used by your primary interface (nic0). Defaults to None.

        subnetwork(str, Optional):
            The URL of the subnetwork to which all instances in the instance group belong. If your instance has multiple network interfaces, then the network and subnetwork fields only refer to the network and subnet used by your primary interface (nic0). Defaults to None.

        named_ports(List[Dict[str, Any]], Optional):
            Assigns a name to a port number. For example: {name: "http", port: 80} This allows the system to reference ports by the assigned name instead of a port number. Named ports can also contain multiple ports. For example: [{name: "app1", port: 8080}, {name: "app1", port: 8081}, {name: "app2", port: 8082}] Named ports apply to all instances in this instance group. . Defaults to None.
                * name(str, Optional):
                    The name for this named port. The name must be 1-63 characters long, and comply with RFC1035.
                * port(int, Optional):
                    The port number, which can be a value between 1 and 65535.

        project(str):
            Project ID for this request.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              gcp.compute.instance_groups.present:
                - name: value
                - zone: value
                - project: value
                - instance_group: value
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    if ctx.get("wrapper_result"):
        result = ctx.get("wrapper_result")

    resource_body = {
        "description": description,
        "zone": zone,
        "name": name,
        "named_ports": named_ports,
        "network": network,
        "subnetwork": subnetwork,
    }

    resource_body = {k: v for (k, v) in resource_body.items() if v is not None}
    operation = None
    if result["old_state"]:
        resource_id = result["old_state"].get("resource_id", None)
        resource_body["resource_id"] = resource_id

        # The fingerprint is required upon an update operation but in the time of creation the
        # resource still do not have fingerprint so, we cannot make it a required param for present method.
        resource_body["fingerprint"] = fingerprint or result["old_state"].get(
            "fingerprint"
        )

        # A dictionary of additional operations to perform on the object identified by the key
        # the values are tuples with the first element - the method to call, the second element - arguments,
        # third - the property is required in the end result
        patch_operations_dict = {
            "named_ports": (
                hub.tool.gcp.compute.instance_group.update_named_ports,
                (ctx, result["old_state"], named_ports),
                True,
            ),
        }

        state_operations = StateOperations(
            hub, "compute.instance_group", patch_operations_dict, result, resource_body
        )

        changes = hub.tool.gcp.utils.compare_states(
            result["old_state"],
            {
                **resource_body,
            },
            "compute.instance_group",
            additional_exclude_paths=list(patch_operations_dict.keys()),
        )

        if changes:
            changed_non_updatable_properties = (
                hub.tool.gcp.resource_prop_utils.get_changed_non_updatable_properties(
                    "compute.instance_group", changes
                )
            )
            if changed_non_updatable_properties:
                result["result"] = False
                result["comment"].append(
                    hub.tool.gcp.comment_utils.non_updatable_properties_comment(
                        "gcp.compute.instance_group",
                        name,
                        changed_non_updatable_properties,
                    )
                )
                result["new_state"] = result["old_state"]
                return result

        if not changes and not any(state_operations.changed_properties_dict.values()):
            result["comment"].append(
                hub.tool.gcp.comment_utils.up_to_date_comment(
                    "gcp.compute.instance_group", name
                )
            )
            result["new_state"] = result["old_state"]
            return result

        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_update_comment(
                    "gcp.compute.instance_group", name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                resource_body
            )
            return result

        state_operations_ret = await state_operations.run_operations()

        if not state_operations_ret["result"] or not state_operations_ret.get(
            "new_state"
        ):
            result["result"] = False
            result["comment"] += state_operations_ret["comment"]
            return result

        result["new_state"] = state_operations_ret["new_state"]
        result["comment"].append(
            hub.tool.gcp.comment_utils.update_comment(
                "gcp.compute.instance_group", name
            )
        )
        return result

    else:
        # Create for test
        if ctx.get("test", False):
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    "gcp.compute.instance_group", name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                resource_body
            )
            result["new_state"][
                "resource_id"
            ] = hub.tool.gcp.resource_prop_utils.construct_resource_id(
                "compute.instance_group", {**locals(), "instanceGroup": name}
            )
            return result

        # Create
        create_ret = await hub.exec.gcp_api.client.compute.instance_group.insert(
            ctx,
            name=name,
            project=project,
            zone=zone,
            request_id=request_id,
            body=resource_body,
        )
        if not create_ret["result"] or not create_ret["ret"]:
            result["result"] = False
            if create_ret["comment"] and next(
                (
                    comment
                    for comment in create_ret["comment"]
                    if "alreadyExists" in comment
                ),
                None,
            ):
                result["comment"].append(
                    hub.tool.gcp.comment_utils.already_exists_comment(
                        "gcp.compute.instance_group", name
                    )
                )
            else:
                result["comment"] += create_ret["comment"]
            return result

        if hub.tool.gcp.operation_utils.is_operation(create_ret["ret"]):
            operation = create_ret["ret"]

    if operation:
        operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            operation.get("selfLink"), "compute.zone_operation"
        )
        result["rerun_data"] = {
            "operation_id": operation_id,
            "old_state": result["old_state"],
        }

    return result


async def absent(
    hub,
    ctx,
    name: str,
    project: str = None,
    zone: str = None,
    request_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Deletes the specified instance group.

    The instances in the group are not deleted. Note that instance group must not belong to a backend service. Read Deleting an instance group for more information.

    Args:
        name(str):
            An Idem name of the resource.

        project(str):
            Project ID for this request.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        zone(str):
            The name of the zone where the instance group is located.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]


    Examples:
        .. code-block:: sls

            resource_is_absent:
              gcp.compute.instance_groups.absent:
                - name: value
                - project: value
                - instance_group: value
                - zone: value
    """
    # the method is handled via the recursive_contracts->call_absent
    raise NotImplementedError


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves the list of zonal instance group resources contained within the specified zone. For managed instance groups, use the instanceGroupManagers or regionInstanceGroupManagers methods instead.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.instance_groups
    """
    result = {}

    describe_ret = await hub.exec.gcp.compute.instance_group.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(
            f"Could not describe gcp.compute.instance_group {describe_ret['comment']}"
        )
        return {}

    for resource in describe_ret["ret"]:
        resource_id = resource.get("resource_id")

        result[resource_id] = {
            "gcp.compute.instance_group.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
