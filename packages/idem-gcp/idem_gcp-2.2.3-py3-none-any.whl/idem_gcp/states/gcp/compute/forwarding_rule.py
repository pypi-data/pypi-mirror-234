"""State module for managing ForwardingRules."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from idem_gcp.tool.gcp.state_operation_utils import StateOperations
from idem_gcp.tool.gcp.utils import regional_absent

# prevent commit hook from removing the import
absent = regional_absent

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    region: str,
    project: str = None,
    forwarding_rule: str = None,
    allow_global_access: bool = None,
    port_range: str = None,
    labels: Dict[str, Any] = None,
    backend_service: str = None,
    description: str = None,
    fingerprint: str = None,
    service_directory_registrations: List[
        make_dataclass(
            "ForwardingRuleServiceDirectoryRegistration",
            [
                ("service", str, field(default=None)),
                ("namespace", str, field(default=None)),
                ("service_directory_region", str, field(default=None)),
            ],
        )
    ] = None,
    ip_protocol: str = None,
    target: str = None,
    ip_version: str = None,
    is_mirroring_collector: bool = None,
    network_tier: str = None,
    no_automate_dns_zone: bool = None,
    ip_address: str = None,
    network: str = None,
    psc_connection_status: str = None,
    label_fingerprint: str = None,
    subnetwork: str = None,
    metadata_filters: List[
        make_dataclass(
            "MetadataFilter",
            [
                ("filter_match_criteria", str, field(default=None)),
                (
                    "filter_labels",
                    List[
                        make_dataclass(
                            "MetadataFilterLabelMatch",
                            [
                                ("name", str, field(default=None)),
                                ("value", str, field(default=None)),
                            ],
                        )
                    ],
                    field(default=None),
                ),
            ],
        )
    ] = None,
    all_ports: bool = None,
    service_label: str = None,
    load_balancing_scheme: str = None,
    ports: List[str] = None,
    request_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Creates or updates a ForwardingRule resource in the specified project and region using the data included in the request.

    Args:
        name(str):
            An Idem name of the resource.

        allow_global_access(bool, Optional):
            This field is used along with the backend_service field for internal load balancing or with the target field for internal TargetInstance. If the field is set to TRUE, clients can access ILB from all regions. Otherwise only allows access from clients in the same region as the internal load balancer. Defaults to None.

        port_range(str, Optional):
            This field can be used only if: - Load balancing scheme is one of EXTERNAL, INTERNAL_SELF_MANAGED or INTERNAL_MANAGED - IPProtocol is one of TCP, UDP, or SCTP. Packets addressed to ports in the specified range will be forwarded to target or backend_service. You can only use one of ports, port_range, or allPorts. The three are mutually exclusive. Forwarding rules with the same [IPAddress, IPProtocol] pair must have disjoint ports. Some types of forwarding target have constraints on the acceptable ports. For more information, see [Port specifications](https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#port_specifications). @pattern: \\d+(?:-\\d+)?. Defaults to None.

        labels(Dict[str, Any], Optional):
            Labels for this resource. These can only be added or modified by the setLabels method. Each label key/value pair must comply with RFC1035. Label values may be empty. Defaults to None.

        backend_service(str, Optional):
            Identifies the backend service to which the forwarding rule sends traffic. Required for Internal TCP/UDP Load Balancing and Network Load Balancing; must be omitted for all other load balancer types. Defaults to None.

        description(str, Optional):
            An optional description of this resource. Provide this property when you create the resource. Defaults to None.

        fingerprint(str, Optional):
            Fingerprint of this resource. A hash of the contents stored in this object. This field is used in optimistic locking. This field will be ignored when inserting a ForwardingRule. Include the fingerprint in patch request to ensure that you do not overwrite changes that were applied from another concurrent request. To see the latest fingerprint, make a get() request to retrieve a ForwardingRule. Defaults to None.

        service_directory_registrations(List[Dict[str, Any]], Optional):
            Service Directory resources to register this forwarding rule with. Currently, only supports a single Service Directory resource. Defaults to None.

            * service(str, Optional):
                Service Directory service to register the forwarding rule under.
            * namespace(str, Optional):
                Service Directory namespace to register the forwarding rule under.
            * service_directory_region(str, Optional):
                [Optional] Service Directory region to register this global forwarding rule under. Default to "us-central1". Only used for PSC for Google APIs. All PSC for Google APIs Forwarding Rules on the same network should use the same Service Directory region.

        ip_protocol(str, Optional):
            The IP protocol to which this rule applies. For protocol forwarding, valid options are TCP, UDP, ESP, AH, SCTP, ICMP and L3_DEFAULT. The valid IP protocols are different for different load balancing products as described in [Load balancing features](https://cloud.google.com/load-balancing/docs/features#protocols_from_the_load_balancer_to_the_backends).
            Enum type. Allowed values:
                "AH"
                "ESP"
                "ICMP"
                "L3_DEFAULT"
                "SCTP"
                "TCP"
                "UDP". Defaults to None.

        target(str, Optional):
            The URL of the target resource to receive the matched traffic. For regional forwarding rules, this target must be in the same region as the forwarding rule. For global forwarding rules, this target must be a global load balancing resource. The forwarded traffic must be of a type appropriate to the target object. For more information, see the "Target" column in [Port specifications](https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications). For Private Service Connect forwarding rules that forward traffic to Google APIs, provide the name of a supported Google API bundle: - vpc-sc - APIs that support VPC Service Controls. - all-apis - All supported Google APIs. . Defaults to None.

        ip_version(str, Optional):
            The IP Version that will be used by this forwarding rule. Valid options are IPV4 or IPV6.
            Enum type. Allowed values:
                "IPV4"
                "IPV6"
                "UNSPECIFIED_VERSION". Defaults to None.

        is_mirroring_collector(bool, Optional):
            Indicates whether or not this load balancer can be used as a collector for packet mirroring. To prevent mirroring loops, instances behind this load balancer will not have their traffic mirrored even if a PacketMirroring rule applies to them. This can only be set to true for load balancers that have their loadBalancingScheme set to INTERNAL. Defaults to None.

        network_tier(str, Optional):
            This signifies the networking tier used for configuring this load balancer and can only take the following values: PREMIUM, STANDARD. For regional ForwardingRule, the valid values are PREMIUM and STANDARD. For GlobalForwardingRule, the valid value is PREMIUM. If this field is not specified, it is assumed to be PREMIUM. If IPAddress is specified, this value must be equal to the networkTier of the Address.
            Enum type. Allowed values:
                "FIXED_STANDARD" - Public internet quality with fixed bandwidth.
                "PREMIUM" - High quality, Google-grade network tier, support for all networking products.
                "STANDARD" - Public internet quality, only limited support for other networking products.
                "STANDARD_OVERRIDES_FIXED_STANDARD" - (Output only) Temporary tier for FIXED_STANDARD when fixed standard tier is expired or not configured. Defaults to None.

        no_automate_dns_zone(bool, Optional):
            This is used in PSC consumer ForwardingRule to control whether it should try to auto-generate a DNS zone or not. Non-PSC forwarding rules do not use this field. Defaults to None.

        ip_address(str, Optional):
            IP address for which this forwarding rule accepts traffic. When a client sends traffic to this IP address, the forwarding rule directs the traffic to the referenced target or backendService. While creating a forwarding rule, specifying an IPAddress is required under the following circumstances: - When the target is set to targetGrpcProxy and validateForProxyless is set to true, the IPAddress should be set to 0.0.0.0. - When the target is a Private Service Connect Google APIs bundle, you must specify an IPAddress. Otherwise, you can optionally specify an IP address that references an existing static (reserved) IP address resource. When omitted, Google Cloud assigns an ephemeral IP address. Use one of the following formats to specify an IP address while creating a forwarding rule: * IP address number, as in `100.1.2.3` * IPv6 address range, as in `2600:1234::/96` * Full resource URL, as in https://www.googleapis.com/compute/v1/projects/ project_id/regions/region/addresses/address-name * Partial URL or by name, as in: - projects/project_id/regions/region/addresses/address-name - regions/region/addresses/address-name - global/addresses/address-name - address-name The forwarding rule's target or backendService, and in most cases, also the loadBalancingScheme, determine the type of IP address that you can use. For detailed information, see [IP address specifications](https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications). When reading an IPAddress, the API always returns the IP address number. Defaults to None.

        network(str, Optional):
            This field is not used for external load balancing. For Internal TCP/UDP Load Balancing, this field identifies the network that the load balanced IP should belong to for this Forwarding Rule. If this field is not specified, the default network will be used. For Private Service Connect forwarding rules that forward traffic to Google APIs, a network must be provided. Defaults to None.

        psc_connection_status(str, Optional):
            Enum type. Allowed values:
                "ACCEPTED" - The connection has been accepted by the producer.
                "CLOSED" - The connection has been closed by the producer and will not serve traffic going forward.
                "NEEDS_ATTENTION" - The connection has been accepted by the producer, but the producer needs to take further action before the forwarding rule can serve traffic.
                "PENDING" - The connection is pending acceptance by the producer.
                "REJECTED" - The connection has been rejected by the producer.
                "STATUS_UNSPECIFIED". Defaults to None.

        label_fingerprint(str, Optional):
            A fingerprint for the labels being applied to this resource, which is essentially a hash of the labels set used for optimistic locking. The fingerprint is initially generated by Compute Engine and changes after every request to modify or update labels. You must always provide an up-to-date fingerprint hash in order to update or change labels, otherwise the request will fail with error 412 conditionNotMet. To see the latest fingerprint, make a get() request to retrieve a ForwardingRule. Defaults to None.

        region(str):
            Name of the region scoping this request.

        subnetwork(str, Optional):
            This field identifies the subnetwork that the load balanced IP should belong to for this Forwarding Rule, used in internal load balancing and network load balancing with IPv6. If the network specified is in auto subnet mode, this field is optional. However, a subnetwork must be specified if the network is in custom subnet mode or when creating external forwarding rule with IPv6. Defaults to None.

        metadata_filters(List[Dict[str, Any]], Optional):
            Opaque filter criteria used by load balancer to restrict routing configuration to a limited set of xDS compliant clients. In their xDS requests to load balancer, xDS clients present node metadata. When there is a match, the relevant configuration is made available to those proxies. Otherwise, all the resources (e.g. TargetHttpProxy, UrlMap) referenced by the ForwardingRule are not visible to those proxies. For each metadataFilter in this list, if its filterMatchCriteria is set to MATCH_ANY, at least one of the filterLabels must match the corresponding label provided in the metadata. If its filterMatchCriteria is set to MATCH_ALL, then all of its filterLabels must match with corresponding labels provided in the metadata. If multiple metadataFilters are specified, all of them need to be satisfied in order to be considered a match. metadataFilters specified here will be applifed before those specified in the UrlMap that this ForwardingRule references. metadataFilters only applies to Loadbalancers that have their loadBalancingScheme set to INTERNAL_SELF_MANAGED. Defaults to None.

            * filter_match_criteria(str, Optional):
                Specifies how individual filter label matches within the list of filterLabels and contributes toward the overall metadataFilter match. Supported values are: - MATCH_ANY: at least one of the filterLabels must have a matching label in the provided metadata. - MATCH_ALL: all filterLabels must have matching labels in the provided metadata.
                Enum type. Allowed values:
                    "MATCH_ALL" - Specifies that all filterLabels must match for the metadataFilter to be considered a match.
                    "MATCH_ANY" - Specifies that any filterLabel must match for the metadataFilter to be considered a match.
                    "NOT_SET" - Indicates that the match criteria was not set. A metadataFilter must never be created with this value.

            * filter_labels(List[Dict[str, Any]], Optional): The list of label value pairs that must match labels in the provided metadata based on filterMatchCriteria This list must not be empty and can have at the most 64 entries.
                * name(str, Optional):
                    Name of metadata label. The name can have a maximum length of 1024 characters and must be at least 1 character long.
                * value(str, Optional):
                    The value of the label must match the specified value. value can have a maximum length of 1024 characters.
        all_ports(bool, Optional):
            This field is used along with the backend_service field for Internal TCP/UDP Load Balancing or Network Load Balancing, or with the target field for internal and external TargetInstance. You can only use one of ports and port_range, or allPorts. The three are mutually exclusive. For TCP, UDP and SCTP traffic, packets addressed to any ports will be forwarded to the target or backendService. Defaults to None.

        service_label(str, Optional):
            An optional prefix to the service name for this Forwarding Rule. If specified, the prefix is the first label of the fully qualified service name. The label must be 1-63 characters long, and comply with RFC1035. Specifically, the label must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. This field is only used for internal load balancing. Defaults to None.

        load_balancing_scheme(str, Optional):
            Specifies the forwarding rule type. For more information about forwarding rules, refer to Forwarding rule concepts.
            Enum type. Allowed values:
                "EXTERNAL"
                "EXTERNAL_MANAGED"
                "INTERNAL"
                "INTERNAL_MANAGED"
                "INTERNAL_SELF_MANAGED"
                "INVALID". Defaults to None.

        ports(List[str], Optional):
            The ports field is only supported when the forwarding rule references a backend_service directly. Only packets addressed to the [specified list of ports]((https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#port_specifications)) are forwarded to backends. You can only use one of ports and port_range, or allPorts. The three are mutually exclusive. You can specify a list of up to five ports, which can be non-contiguous. Forwarding rules with the same [IPAddress, IPProtocol] pair must have disjoint ports. @pattern: \\d+(?:-\\d+)?. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        project(str):
            Project ID for this request.

        forwarding_rule(str):
            Name of the ForwardingRule resource to return.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              gcp.compute.forwarding_rules.present:
                - name: value
                - region: value
                - project: value
                - forwarding_rule: value
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
        "name": name,
        "description": description,
        "region": region,
        "forwarding_rule": forwarding_rule,
        "allow_global_access": allow_global_access,
        "port_range": port_range,
        "backend_service": backend_service,
        "metadata_filters": metadata_filters,
        "service_directory_registrations": service_directory_registrations,
        "ip_protocol": ip_protocol,
        "ip_version": ip_version,
        "is_mirroring_collector": is_mirroring_collector,
        "network_tier": network_tier,
        "no_automate_dns_zone": no_automate_dns_zone,
        "ip_address": ip_address,
        "network": network,
        "psc_connection_status": psc_connection_status,
        "subnetwork": subnetwork,
        "all_ports": all_ports,
        "service_label": service_label,
        "load_balancing_scheme": load_balancing_scheme,
        "ports": ports,
        "target": target,
        "labels": labels,
        "label_fingerprint": label_fingerprint,
    }

    resource_body = {k: v for (k, v) in resource_body.items() if v is not None}
    operation = None
    if result["old_state"]:
        resource_id = result["old_state"].get("resource_id", None)
        resource_body["resource_id"] = resource_id
        # The fingerprint is required upon an update operation but in the time of creation the
        # resource still do not have fingerprint so, we cannot make it a required param for present method.
        new_fingerprint = fingerprint or result["old_state"].get("fingerprint")
        if new_fingerprint:
            resource_body["fingerprint"] = new_fingerprint

        new_label_fingerprint = label_fingerprint or result["old_state"].get(
            "label_fingerprint"
        )
        if new_label_fingerprint:
            resource_body["label_fingerprint"] = new_label_fingerprint

        patch_operations_dict = {
            "target": (
                hub.exec.gcp.compute.forwarding_rule.set_target,
                (ctx, target, name, project, region, resource_id),
                False,
                True,
            ),
            "labels": (
                hub.exec.gcp.compute.forwarding_rule.set_labels,
                (ctx, labels, label_fingerprint, resource_id, project, region),
                False,
                True,
            ),
        }

        state_operations = StateOperations(
            hub, "compute.forwarding_rule", patch_operations_dict, result, resource_body
        )

        changes = hub.tool.gcp.utils.compare_states(
            result["old_state"],
            {
                "resource_id": resource_id,
                **resource_body,
            },
            "compute.forwarding_rule",
            additional_exclude_paths=list(patch_operations_dict.keys()),
        )

        if not changes and not any(state_operations.changed_properties_dict.values()):
            result["comment"].append(
                hub.tool.gcp.comment_utils.up_to_date_comment(
                    "gcp.compute.forwarding_rule", name
                )
            )
            result["new_state"] = result["old_state"]
            return result

        changed_non_updatable_properties = (
            hub.tool.gcp.resource_prop_utils.get_changed_non_updatable_properties(
                "compute.forwarding_rule", changes
            )
        )

        if changed_non_updatable_properties:
            result["result"] = False
            result["comment"].append(
                hub.tool.gcp.comment_utils.non_updatable_properties_comment(
                    "gcp.compute.forwarding_rule",
                    name,
                    changed_non_updatable_properties,
                )
            )
            result["new_state"] = result["old_state"]
            return result

        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_update_comment(
                    "gcp.compute.forwarding_rule", name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                resource_body
            )
            return result

        state_operations_ret = await state_operations.run_operations()

        if not state_operations_ret["result"]:
            result["comment"] += state_operations_ret["comment"]
            result["result"] = False
            return result
        elif "new_state" in state_operations_ret:
            result["new_state"] = state_operations_ret["new_state"]

        if changes:
            # Perform update
            update_ret = await hub.exec.gcp_api.client.compute.forwarding_rule.patch(
                hub,
                ctx,
                name=name,
                resource_id=resource_id,
                request_id=request_id,
                # as per the docs only the network tier can be changed
                body={"network_tier": network_tier},
            )
            if not update_ret["result"] or not update_ret["ret"]:
                result["result"] = False
                result["comment"] += update_ret["comment"]
                return result

            if "compute#operation" in update_ret["ret"].get("kind", ""):
                operation = update_ret["ret"]
    else:
        if ctx.get("test", False):
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    "gcp.compute.forwarding_rule", name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                resource_body
            )
            result["new_state"]["resource_id"] = resource_id
            return result

        # Create
        create_ret = await hub.exec.gcp_api.client.compute.forwarding_rule.insert(
            ctx,
            name=name,
            project=project,
            region=region,
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
                        "gcp.compute.forwarding_rule", name
                    )
                )
            else:
                result["comment"] += create_ret["comment"]
            return result

        if "compute#operation" in create_ret["ret"].get("kind", ""):
            operation = create_ret["ret"]

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

    Retrieves the list of ForwardingRule resources available to the specified project.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.forwarding_rule
    """
    result = {}

    describe_ret = await hub.exec.gcp.compute.forwarding_rule.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(
            f"Could not describe gcp.compute.forwarding_rule {describe_ret['comment']}"
        )
        return {}

    for resource in describe_ret["ret"]:
        resource_id = resource.get("resource_id")

        # for global forwarding rules we can't compute the resource_id
        if resource_id:
            result[resource_id] = {
                "gcp.compute.forwarding_rule.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource.items()
                ]
            }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
