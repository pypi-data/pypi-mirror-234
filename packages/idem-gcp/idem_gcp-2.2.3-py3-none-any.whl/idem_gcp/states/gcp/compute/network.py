"""State module for managing Networks."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from dict_tools.typing import Computed

from idem_gcp.tool.gcp.utils import global_absent

# prevent commit hook from removing the import
absent = global_absent

__contracts__ = ["resource"]
RESOURCE_TYPE = "compute.network"
RESOURCE_TYPE_FULL = "gcp.compute.network"


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    request_id: str = None,
    project: str = None,
    auto_create_subnetworks: bool = None,
    description: str = None,
    enable_ula_internal_ipv6: bool = None,
    internal_ipv6_range: str = None,
    mtu: int = None,
    network_firewall_policy_enforcement_order: str = None,
    routing_config: make_dataclass(
        "NetworkRoutingConfig",
        [
            ("routing_mode", str, field(default=None)),
        ],
    ) = None,
    peerings: List[
        make_dataclass(
            "NetworkPeering",
            [
                ("export_custom_routes", bool, field(default=None)),
                ("auto_create_routes", bool, field(default=None)),
                ("network", str, field(default=None)),
                ("name", str, field(default=None)),
                ("state", str, field(default=None)),
                ("peer_mtu", int, field(default=None)),
                ("import_subnet_routes_with_public_ip", bool, field(default=None)),
                ("import_custom_routes", bool, field(default=None)),
                ("state_details", str, field(default=None)),
                ("export_subnet_routes_with_public_ip", bool, field(default=None)),
                ("exchange_subnet_routes", bool, field(default=None)),
                ("stack_type", str, field(default=None)),
            ],
        )
    ] = None,
    id_: (Computed[str], "alias=id") = None,
) -> Dict[str, Any]:
    r"""Creates a network in the specified project using the data included in the request.

    Args:
        name(str):
            An Idem name of the resource.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        project(str, Optional):
            Project ID for this request.

        routing_config(NetworkRoutingConfig, Optional):
            The network-level routing configuration for this network. Used by Cloud Router to determine what type of network-wide routing behavior to enforce. Defaults to None.

            * routing_mode(str, Optional):
                The network-wide routing mode to use. If set to REGIONAL, this network's Cloud Routers will only advertise routes with subnets of this network in the same
                region as the router. If set to GLOBAL, this network's Cloud Routers will advertise routes with all subnets of this network, across regions.
                Enum type. Allowed values:
                    "GLOBAL"
                    "REGIONAL"

        description(str, Optional):
            An optional description of this resource. Provide this field when you create the resource. Defaults to None.

        auto_create_subnetworks(bool, Optional):
            Must be set to create a VPC network. If not set, a legacy network is created. When set to true, the VPC network is created in auto mode. When set to false, the VPC network is created in custom mode. An auto mode VPC network starts with one subnet per region. Each subnet has a predetermined range as described in Auto mode VPC network IP ranges. For custom mode VPC networks, you can add subnets using the subnetworks insert method. Defaults to None.

        internal_ipv6_range(str, Optional):
            When enabling ula internal ipv6, caller optionally can specify the /48 range they want from the google defined ULA prefix fd20::/20. The input must be a valid /48 ULA IPv6 address and must be within the fd20::/20. Operation will fail if the speficied /48 is already in used by another resource. If the field is not speficied, then a /48 range will be randomly allocated from fd20::/20 and returned via this field. . Defaults to None.

        network_firewall_policy_enforcement_order(str, Optional):
            The network firewall policy enforcement order. Can be either AFTER_CLASSIC_FIREWALL or BEFORE_CLASSIC_FIREWALL. Defaults to AFTER_CLASSIC_FIREWALL if the field is not specified. Defaults to None.

        enable_ula_internal_ipv6(bool, Optional):
            Enable ULA internal ipv6 on this network. Enabling this feature will assign a /48 from google defined ULA prefix fd20::/20. . Defaults to None.

        mtu(int, Optional):
            Maximum Transmission Unit in bytes. The minimum value for this field is 1300 and the maximum value is 8896. The suggested value is 1500, which is the default MTU used on the Internet, or 8896 if you want to use Jumbo frames. If unspecified, the value defaults to 1460. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        peerings(List[Dict[str, Any]], Optional):
            A list of network peerings for the resource. Defaults to None.

            * export_custom_routes(bool, Optional):
                Whether to export the custom routes to peer network. The default value is false.
            * auto_create_routes(bool, Optional):
                This field will be deprecated soon. Use the exchange_subnet_routes field instead. Indicates whether full mesh connectivity is created and managed automatically between peered networks. Currently this field should always be true since Google Compute Engine will automatically create and manage subnetwork routes between two networks when peering state is ACTIVE.
            * network(str, Optional):
                The URL of the peer network. It can be either full URL or partial URL. The peer network may belong to a different project. If the partial URL does not contain project, it is assumed that the peer network is in the same project as the current network.
            * name(str, Optional):
                Name of this peering. Provided by the client when the peering is created. The name must comply with RFC1035. Specifically, the name must be 1-63 characters long and match regular expression `[a-z]([-a-z0-9]*[a-z0-9])?`. The first character must be a lowercase letter, and all the following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
            * state(str, Optional):
                [Output Only] State for the peering, either `ACTIVE` or `INACTIVE`. The peering is `ACTIVE` when there's a matching configuration in the peer network.
                Enum type. Allowed values:
                    "ACTIVE" - Matching configuration exists on the peer.
                    "INACTIVE" - There is no matching configuration on the peer, including the case when peer does not exist.
            * peer_mtu(int, Optional):
                Maximum Transmission Unit in bytes.
            * import_subnet_routes_with_public_ip(bool, Optional):
                Whether subnet routes with public IP range are imported. The default value is false. IPv4 special-use ranges are always imported from peers and are not controlled by this field.
            * import_custom_routes(bool, Optional):
                Whether to import the custom routes from peer network. The default value is false.
            * state_details(str, Optional):
                [Output Only] Details about the current state of the peering.
            * export_subnet_routes_with_public_ip(bool, Optional):
                Whether subnet routes with public IP range are exported. The default value is true, all subnet routes are exported. IPv4 special-use ranges are always exported to peers and are not controlled by this field.
            * exchange_subnet_routes(bool, Optional):
                Indicates whether full mesh connectivity is created and managed automatically between peered networks. Currently this field should always be true since Google Compute Engine will automatically create and manage subnetwork routes between two networks when peering state is ACTIVE.
            * stack_type(str, Optional):
                Which IP version(s) of traffic and routes are allowed to be imported or exported between peer networks. The default value is IPV4_ONLY.
                Enum type. Allowed values:
                    "IPV4_IPV6" - This Peering will allow IPv4 traffic and routes to be exchanged. Additionally if the matching peering is IPV4_IPV6, IPv6 traffic and routes will be exchanged as well.
                    "IPV4_ONLY" - This Peering will only allow IPv4 traffic and routes to be exchanged, even if the matching peering is IPV4_IPV6.

        id(str, Optional): The unique identifier for the resource. This identifier is defined by the server. Read-only property

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            example_resource_name:
              gcp.compute.network.present:
                - project: project-name
                - auto_create_subnetworks: false
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)
    resource_type_camel = hub.tool.gcp.case.camel(RESOURCE_TYPE_FULL.split(".")[-1])

    if hub.tool.gcp.resource_prop_utils.properties_mismatch_resource_id(
        RESOURCE_TYPE, resource_id, {**locals(), resource_type_camel: name}
    ):
        result["comment"].append(
            hub.tool.gcp.comment_utils.properties_mismatch_resource_id_comment(
                RESOURCE_TYPE_FULL, name
            )
        )

    if ctx.get("rerun_data"):
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            ctx, ctx.get("rerun_data"), "compute.network"
        )

        if not handle_operation_ret["result"]:
            result["comment"] += handle_operation_ret["comment"]
            if handle_operation_ret.get("rerun_data"):
                result["rerun_data"] = handle_operation_ret["rerun_data"]
                if handle_operation_ret["rerun_data"].get("has_error", False):
                    result["result"] = False
            else:
                result["result"] = False

            return result

        resource_id = handle_operation_ret["resource_id"]

    get_resource_only_with_resource_id = hub.OPT.idem.get(
        "get_resource_only_with_resource_id", False
    )
    if resource_id:
        old_get_ret = await hub.exec.gcp.compute.network.get(
            ctx, resource_id=resource_id
        )

        if not old_get_ret["result"] or (
            not old_get_ret["ret"] and get_resource_only_with_resource_id
        ):
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        # long running operation has succeeded - both update and create
        if ctx.get("rerun_data"):
            result["new_state"] = old_get_ret["ret"]
            result["old_state"] = ctx["rerun_data"]["old_state"]
            if ctx["rerun_data"]["old_state"]:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.update_comment(
                        "gcp.compute.network", name
                    )
                )
            else:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.create_comment(
                        "gcp.compute.network", name
                    )
                )
                # Handle the peerings addition when new network is created
                if not result["new_state"].get("peerings") and peerings:
                    add_peerings_ret = await hub.tool.gcp.compute.network.add_peerings(
                        ctx, resource_id, peerings
                    )
                    if not add_peerings_ret["result"]:
                        result["result"] = False
                        result["comment"] += add_peerings_ret["comment"]
                        return result

                # Make a new get request containing the peerings in their form in gcp api
                get_ret = await hub.exec.gcp_api.client.compute.network.get(
                    ctx, name=name, resource_id=resource_id
                )
                if not get_ret["result"] and not get_ret["ret"]:
                    result["result"] = False
                    result["comment"] += get_ret["comment"]
                    return result
                result["new_state"] = get_ret["ret"]

            return result

        result["old_state"] = old_get_ret["ret"]
    elif not get_resource_only_with_resource_id:
        resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
            "compute.network", {**locals(), "network": name}
        )
        old_get_ret = await hub.exec.gcp.compute.network.get(
            ctx, resource_id=resource_id
        )
        if not old_get_ret["result"]:
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        if old_get_ret["ret"]:
            result["old_state"] = old_get_ret["ret"]

    request_body = {
        "name": name,
        "description": description,
        "auto_create_subnetworks": auto_create_subnetworks,
        "enable_ula_internal_ipv6": enable_ula_internal_ipv6,
        "internal_ipv6_range": internal_ipv6_range,
        "mtu": mtu,
        "network_firewall_policy_enforcement_order": network_firewall_policy_enforcement_order,
        "routing_config": routing_config,
        "peerings": peerings,
        "id_": id_,
    }

    request_body = {k: v for (k, v) in request_body.items() if v is not None}
    operation = None
    if result["old_state"]:
        changes = hub.tool.gcp.utils.compare_states(
            result["old_state"],
            request_body,
            "compute.network",
        )
        if changes:
            changed_non_updatable_properties = (
                hub.tool.gcp.resource_prop_utils.get_changed_non_updatable_properties(
                    "compute.network", changes
                )
            )
            if changed_non_updatable_properties:
                result["result"] = False
                result["comment"].append(
                    hub.tool.gcp.comment_utils.non_updatable_properties_comment(
                        "gcp.compute.network",
                        name,
                        changed_non_updatable_properties,
                    )
                )
                result["new_state"] = result["old_state"]
                return result

        peerings = hub.tool.gcp.compute.network.build_new_peerings_on_top_of_old(
            result["old_state"].get("peerings"), peerings
        )

        # We want to make sure that the network in the current and new peerings have the same format.
        for peering in result["old_state"].get("peerings", []):
            peering[
                "network"
            ] = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                peering["network"], "compute.network"
            )
        for peering in peerings or []:
            peering[
                "network"
            ] = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                peering["network"], "compute.network"
            )

        peerings_changes = None
        if peerings is not None:
            request_body["peerings"] = peerings
            peerings_changes = hub.tool.gcp.utils.compare_states(
                {"peerings": result["old_state"].get("peerings") or []},
                {"peerings": peerings},
                resource_type=None,
                additional_exclude_paths=[
                    "peerings[].peer_mtu",
                    "peerings[].auto_create_routes",
                ],
            )

        if not changes and not peerings_changes:
            result["result"] = True
            result["comment"].append(
                hub.tool.gcp.comment_utils.up_to_date_comment(
                    "gcp.compute.network", name
                )
            )
            result["new_state"] = result["old_state"]
            return result

        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_update_comment(
                    "gcp.compute.network", name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                {"resource_id": resource_id, **request_body}
            )
            return result

        if peerings_changes:
            update_peerings_ret = await hub.tool.gcp.compute.network.update_peerings(
                ctx, resource_id, result["old_state"].get("peerings"), peerings
            )
            if not update_peerings_ret["result"]:
                result["result"] = False
                result["comment"] += update_peerings_ret["comment"]
                return result

        if changes:
            if peerings_changes:
                get_ret = await hub.exec.gcp.compute.network.get(
                    ctx, resource_id=resource_id
                )
                if not get_ret["result"] and not get_ret["ret"]:
                    result["result"] = False
                    result["comment"] += get_ret["comment"]
                    return result

                # The peerings should be the same so update does not happen there
                request_body["peerings"] = get_ret["ret"].get("peerings")

            patch_ret = await hub.exec.gcp_api.client.compute.network.patch(
                ctx, resource_id=resource_id, body=request_body
            )

            if not patch_ret["result"]:
                result["result"] = False
                result["comment"] += patch_ret["comment"]
                return result
            if patch_ret["ret"] is not None:
                if hub.tool.gcp.operation_utils.is_operation(patch_ret["ret"]):
                    operation = patch_ret["ret"]

        get_ret = await hub.exec.gcp.compute.network.get(ctx, resource_id=resource_id)
        if not get_ret["result"] and not get_ret["ret"]:
            result["result"] = False
            result["comment"] += get_ret["comment"]
            return result

        result["new_state"] = get_ret["ret"]
        result["comment"].append(
            hub.tool.gcp.comment_utils.update_comment("gcp.compute.network", name)
        )
    else:
        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    "gcp.compute.network", name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                {"resource_id": resource_id, **request_body}
            )
            return result

        create_ret = await hub.exec.gcp_api.client.compute.network.insert(
            ctx, name=name, project=project, body=request_body
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
                        "gcp.compute.network", name
                    )
                )
            else:
                result["comment"] += create_ret["comment"]
            return result

        if hub.tool.gcp.operation_utils.is_operation(create_ret.get("ret")):
            operation = create_ret["ret"]

    if operation:
        operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            operation.get("selfLink"), "compute.global_operation"
        )
        result["rerun_data"] = {
            "operation_id": operation_id,
            "old_state": result["old_state"],
        }

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves the list of networks available to the specified project.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.network

    """
    result = {}

    # TODO: Pagination
    describe_ret = await hub.exec.gcp_api.client.compute.network.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(
            f"Could not describe gcp.compute.network {describe_ret['comment']}"
        )
        return {}

    for resource in describe_ret["ret"].get("items", []):
        resource_id = resource.get("resource_id")

        result[resource_id] = {
            "gcp.compute.network.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
