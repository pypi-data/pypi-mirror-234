"""State module for managing subnetworks."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from dict_tools.typing import Computed

from idem_gcp.tool.gcp.utils import regional_absent

# prevent commit hook from removing the import
absent = regional_absent

from idem_gcp.tool.gcp.state_operation_utils import StateOperations

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    region: str = None,
    project: str = None,
    request_id: str = None,
    enable_flow_logs: bool = None,
    private_ip_google_access: bool = None,
    description: str = None,
    network: str = None,
    stack_type: str = None,
    log_config: make_dataclass(
        "SubnetworkLogConfig",
        [
            ("aggregation_interval", str, field(default=None)),
            ("filter_expr", str, field(default=None)),
            ("enable", bool, field(default=None)),
            ("flow_sampling", float, field(default=None)),
            ("metadata_fields", List[str], field(default=None)),
            ("metadata", str, field(default=None)),
        ],
    ) = None,
    role: str = None,
    ipv6_access_type: str = None,
    fingerprint: str = None,
    secondary_ip_ranges: List[
        make_dataclass(
            "SubnetworkSecondaryRange",
            [
                ("ip_cidr_range", str, field(default=None)),
                ("range_name", str, field(default=None)),
            ],
        )
    ] = None,
    purpose: str = None,
    private_ipv6_google_access: str = None,
    ip_cidr_range: str = None,
    drain_timeout_seconds: int = None,
    resource_id: str = None,
    id_: (Computed[str], "alias=id") = None,
) -> Dict[str, Any]:
    r"""Creates a subnetwork in the specified project using the data included in the request.

    Args:
        name(str):
            An Idem name of the resource.

        project(str, Optional):
            Project ID for this request.

        region(str, Optional):
            Name of the region scoping this request.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        enable_flow_logs(bool, Optional):
            Whether to enable flow logging for this subnetwork. If this field is not explicitly set, it will not appear in get listings. If not set the default behavior is determined by the org policy, if there is no org policy specified, then it will default to disabled. This field isn't supported with the purpose field set to INTERNAL_HTTPS_LOAD_BALANCER. Defaults to None.

        private_ip_google_access(bool, Optional):
            Whether the VMs in this subnet can access Google services without assigned external IP addresses. This field can be both set at resource creation time and updated using setPrivateIpGoogleAccess. Defaults to None.

        description(str, Optional):
            An optional description of this resource. Provide this property when you create the resource. This field can be set only at resource creation time. Defaults to None.

        network(str, Optional):
            The URL of the network to which this subnetwork belongs, provided by the client when initially creating the subnetwork. This field can be set only at resource creation time. Defaults to None.

        stack_type(str, Optional):
            The stack type for the subnet. If set to IPV4_ONLY, new VMs in the subnet are assigned IPv4 addresses only. If set to IPV4_IPV6, new VMs in the subnet can be assigned both IPv4 and IPv6 addresses. If not specified, IPV4_ONLY is used. This field can be both set at resource creation time and updated using patch.
            Enum type. Allowed values:
                "IPV4_IPV6" - New VMs in this subnet can have both IPv4 and IPv6 addresses.
                "IPV4_ONLY" - New VMs in this subnet will only be assigned IPv4 addresses. Defaults to None.

        log_config(Dict[str, Any], Optional):
            This field denotes the VPC flow logging options for this subnetwork. If logging is enabled, logs are exported to Cloud Logging.
            SubnetworkLogConfig: The available logging options for this subnetwork. Defaults to None.

            * aggregation_interval(str, Optional):
                Can only be specified if VPC flow logging for this subnetwork is enabled. Toggles the aggregation interval for collecting flow logs. Increasing the interval time will reduce the amount of generated flow logs for long lasting connections. Default is an interval of 5 seconds per connection.
                Enum type. Allowed values:
                    "INTERVAL_10_MIN"
                    "INTERVAL_15_MIN"
                    "INTERVAL_1_MIN"
                    "INTERVAL_30_SEC"
                    "INTERVAL_5_MIN"
                    "INTERVAL_5_SEC"

            * filter_expr(str, Optional):
                Can only be specified if VPC flow logs for this subnetwork is enabled. The filter expression is used to define which VPC flow logs should be exported to Cloud Logging.

            * enable(bool, Optional):
                Whether to enable flow logging for this subnetwork. If this field is not explicitly set, it will not appear in get listings. If not set the default behavior is determined by the org policy, if there is no org policy specified, then it will default to disabled.

            * flow_sampling(float, Optional):
                Can only be specified if VPC flow logging for this subnetwork is enabled. The value of the field must be in [0, 1]. Set the sampling rate of VPC flow logs within the subnetwork where 1.0 means all collected logs are reported and 0.0 means no logs are reported. Default is 0.5 unless otherwise specified by the org policy, which means half of all collected logs are reported.

            * metadata_fields(List[str], Optional):
                Can only be specified if VPC flow logs for this subnetwork is enabled and "metadata" was set to CUSTOM_METADATA.

            * metadata(str, Optional):
                Can only be specified if VPC flow logs for this subnetwork is enabled. Configures whether all, none or a subset of metadata fields should be added to the reported VPC flow logs. Default is EXCLUDE_ALL_METADATA.
                Enum type. Allowed values:
                    "CUSTOM_METADATA"
                    "EXCLUDE_ALL_METADATA"
                    "INCLUDE_ALL_METADATA"

        role(str, Optional):
            The role of subnetwork. Currently, this field is only used when purpose = INTERNAL_HTTPS_LOAD_BALANCER. The value can be set to ACTIVE or BACKUP. An ACTIVE subnetwork is one that is currently being used for Internal HTTP(S) Load Balancing. A BACKUP subnetwork is one that is ready to be promoted to ACTIVE or is currently draining. This field can be updated with a patch request.
            Enum type. Allowed values:
                "ACTIVE" - The ACTIVE subnet that is currently used.
                "BACKUP" - The BACKUP subnet that could be promoted to ACTIVE. Defaults to None.

        ipv6_access_type(str, Optional):
            The access type of IPv6 address this subnet holds. It's immutable and can only be specified during creation or the first time the subnet is updated into IPV4_IPV6 dual stack.
            Enum type. Allowed values:
                "EXTERNAL" - VMs on this subnet will be assigned IPv6 addresses that are accessible via the Internet, as well as the VPC network.
                "INTERNAL" - VMs on this subnet will be assigned IPv6 addresses that are only accessible over the VPC network. Defaults to None.

        fingerprint(str, Optional):
            Fingerprint of this resource. A hash of the contents stored in this object. This field is used in optimistic locking. This field will be ignored when inserting a Subnetwork. An up-to-date fingerprint must be provided in order to update the Subnetwork, otherwise the request will fail with error 412 conditionNotMet. To see the latest fingerprint, make a get() request to retrieve a Subnetwork. Defaults to None.

        secondary_ip_ranges(List[Dict[str, Any]], Optional):
            An array of configurations for secondary IP ranges for VM instances contained in this subnetwork. The primary IP of such VM must belong to the primary ipCidrRange of the subnetwork. The alias IPs may belong to either primary or secondary ranges. This field can be updated with a patch request. Defaults to None.

            * ip_cidr_range(str, Optional):
                The range of IP addresses belonging to this subnetwork secondary range. Provide this property when you create the subnetwork. Ranges must be unique and non-overlapping with all primary and secondary IP ranges within a network. Only IPv4 is supported. The range can be any range listed in the Valid ranges list.
            * range_name(str, Optional):
                The name associated with this subnetwork secondary range, used when adding an alias IP range to a VM instance. The name must be 1-63 characters long, and comply with RFC1035. The name must be unique within the subnetwork.

        purpose(str, Optional):
            The purpose of the resource. This field can be either PRIVATE_RFC_1918 or INTERNAL_HTTPS_LOAD_BALANCER. A subnetwork with purpose set to INTERNAL_HTTPS_LOAD_BALANCER is a user-created subnetwork that is reserved for Internal HTTP(S) Load Balancing. If unspecified, the purpose defaults to PRIVATE_RFC_1918. The enableFlowLogs field isn't supported with the purpose field set to INTERNAL_HTTPS_LOAD_BALANCER.
            Enum type. Allowed values:
                "INTERNAL_HTTPS_LOAD_BALANCER" - Subnet reserved for Internal HTTP(S) Load Balancing.
                "PRIVATE" - Regular user created or automatically created subnet.
                "PRIVATE_RFC_1918" - Regular user created or automatically created subnet.
                "PRIVATE_SERVICE_CONNECT" - Subnetworks created for Private Service Connect in the producer network.
                "REGIONAL_MANAGED_PROXY" - Subnetwork used for Regional Internal/External HTTP(S) Load Balancing. Defaults to None.

        private_ipv6_google_access(str, Optional):
            This field is for internal use. This field can be both set at resource creation time and updated using patch.
            Enum type. Allowed values:
                "DISABLE_GOOGLE_ACCESS" - Disable private IPv6 access to/from Google services.
                "ENABLE_BIDIRECTIONAL_ACCESS_TO_GOOGLE" - Bidirectional private IPv6 access to/from Google services.
                "ENABLE_OUTBOUND_VM_ACCESS_TO_GOOGLE" - Outbound private IPv6 access from VMs in this subnet to Google services. Defaults to None.

        ip_cidr_range(str, Optional):
            The range of internal addresses that are owned by this subnetwork. Provide this property when you create the subnetwork. For example, 10.0.0.0/8 or 100.64.0.0/10. Ranges must be unique and non-overlapping within a network. Only IPv4 is supported. This field is set at resource creation time. The range can be any range listed in the Valid ranges list. The range can be expanded after creation using expandIpCidrRange. Defaults to None.

        drain_timeout_seconds(int, Optional):
            The drain timeout specifies the upper bound in seconds on the amount of time allowed to drain connections from the current ACTIVE subnetwork to the current BACKUP subnetwork. The drain timeout is only applicable when the following conditions are true: - the subnetwork being patched has purpose = INTERNAL_HTTPS_LOAD_BALANCER - the subnetwork being patched has role = BACKUP - the patch request is setting the role to ACTIVE. Note that after this patch operation the roles of the ACTIVE and BACKUP subnetworks will be swapped. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        id(str, Optional): The unique identifier for the resource. This identifier is defined by the server. Read-only property

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            example_resource_name:
              gcp.compute.subnetwork.present:
                - name: value
                - region: value
                - project: value
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

    request_body = {
        "log_config": log_config,
        "purpose": purpose,
        "private_ipv6_google_access": private_ipv6_google_access,
        "private_ip_google_access": private_ip_google_access,
        "role": role,
        "ipv6_access_type": ipv6_access_type,
        "name": name,
        "ip_cidr_range": ip_cidr_range,
        "description": description,
        "enable_flow_logs": enable_flow_logs,
        "stack_type": stack_type,
        "secondary_ip_ranges": secondary_ip_ranges,
        "network": network,
        "id_": id_,
    }

    operation = None
    plan_state = {"resource_id": resource_id, **request_body}
    plan_state = {k: v for (k, v) in plan_state.items() if v is not None}

    if result["old_state"]:
        resource_id = result["old_state"].get("resource_id", None)
        # Update subnetwork
        patch_operations_dict = {
            "ip_cidr_range": (
                hub.tool.gcp.compute.subnetwork.update_ip_cidr_range,
                (ctx, result["old_state"], ip_cidr_range),
                True,
            ),
        }

        state_operations = StateOperations(
            hub, "compute.subnetwork", patch_operations_dict, result, request_body
        )

        changes = hub.tool.gcp.utils.compare_states(
            result["old_state"],
            {
                "resource_id": resource_id,
                **request_body,
            },
            "compute.subnetwork",
            additional_exclude_paths=list(patch_operations_dict.keys()),
        )

        if not changes and not any(state_operations.changed_properties_dict.values()):
            result["result"] = True
            result["comment"].append(
                hub.tool.gcp.comment_utils.up_to_date_comment(
                    "gcp.compute.subnetwork", name
                )
            )
            result["new_state"] = result["old_state"]
            return result

        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_update_comment(
                    "gcp.compute.subnetwork", name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                plan_state
            )
            return result

        state_operations_ret = await state_operations.run_operations()

        if not state_operations_ret["result"]:
            result["comment"] += state_operations_ret["comment"]
            result["result"] = False
            return result

        if changes:
            if any(state_operations.changed_properties_dict.values()):
                get_ret = await hub.exec.gcp.compute.subnetwork.get(
                    ctx, name=name, resource_id=resource_id
                )

                if not get_ret["result"] and not get_ret["ret"]:
                    result["result"] = False
                    result["comment"] += get_ret["comment"]
                    return result

                for k in patch_operations_dict.keys():
                    request_body[k] = get_ret["ret"].get(k)

                request_body["fingerprint"] = get_ret["ret"].get("fingerprint")

            body = (
                {**request_body, "fingerprint": result["old_state"].get("fingerprint")}
                if not request_body.get("fingerprint")
                else {**request_body}
            )
            body.pop("ip_cidr_range")
            body.pop("network")
            state_operations.pre_process_resource_body(body)
            update = await hub.exec.gcp_api.client.compute.subnetwork.patch(
                ctx, resource_id=resource_id, body=body
            )
            if not update["result"]:
                result["result"] = False
                result["comment"] += update["comment"]
                return result

            if hub.tool.gcp.operation_utils.is_operation(update["ret"]):
                operation = update["ret"]

        if not changes and any(state_operations.changed_properties_dict.values()):
            get_ret = await hub.exec.gcp.compute.subnetwork.get(
                ctx, name=name, resource_id=resource_id
            )
            if not get_ret["result"] and not get_ret["ret"]:
                result["result"] = False
                result["comment"] += get_ret["comment"]
                return result

            result["new_state"] = get_ret["ret"]
            result["comment"].append(
                hub.tool.gcp.comment_utils.update_comment(
                    "gcp.compute.subnetwork", name
                )
            )
            return result
    else:
        # Create subnetwork
        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    "gcp.compute.subnetwork", name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                plan_state
            )
            result["new_state"][
                "resource_id"
            ] = hub.tool.gcp.resource_prop_utils.construct_resource_id(
                "compute.subnetwork", {**locals(), "subnetwork": name}
            )
            return result

        create = await hub.exec.gcp_api.client.compute.subnetwork.insert(
            ctx, project=project, region=region, body=request_body
        )
        if not create["result"]:
            result["result"] = False
            result["comment"] += create["comment"]
            return result

        if hub.tool.gcp.operation_utils.is_operation(create["ret"]):
            operation = create["ret"]

    if operation:
        operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            operation.get("selfLink"), "compute.region_operation"
        )
        result["rerun_data"] = {
            "operation_id": operation_id,
            "old_state": result["old_state"],
        }
        return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves a list of subnetworks available to the specified project.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.subnetwork
    """
    result = {}

    list_result = await hub.exec.gcp.compute.subnetwork.list(
        ctx, project=ctx.acct.project_id
    )

    if not list_result["result"]:
        hub.log.debug(f"Could not describe subnetworks {list_result['comment']}")
        return {}

    for resource in list_result["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "gcp.compute.subnetwork.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
