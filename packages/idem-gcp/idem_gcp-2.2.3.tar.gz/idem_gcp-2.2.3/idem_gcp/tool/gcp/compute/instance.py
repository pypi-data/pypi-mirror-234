import copy
from typing import Any
from typing import Dict
from typing import List


async def update_network_interfaces(
    hub,
    ctx,
    current_instance: Dict[str, Any],
    new_network_interfaces: List[Dict[str, Any]],
) -> Dict[str, Any]:
    # Update the updatable network interface properties and the access configs
    result = {"result": True, "comment": []}

    existing_network_interfaces = current_instance.get("network_interfaces", [])

    changed_interfaces = {}

    # validate no network interfaces were added
    for new_network_interface in new_network_interfaces:
        interface_name = new_network_interface.get("name")
        existing_network_interface = next(
            (
                existing_interface
                for existing_interface in existing_network_interfaces
                if existing_interface.get("name") == interface_name
            ),
            None,
        )
        if not existing_network_interface:
            result["result"] = False
            result["comment"].append(
                f"Network interface addition not supported for interface {interface_name}"
            )
        else:
            changed_interfaces[interface_name] = {
                "existing": existing_network_interface,
                "new": new_network_interface,
            }
            if len(new_network_interface.get("access_configs", [])) > 1:
                result["result"] = False
                result["comment"].append(
                    f"Network interface {interface_name} cannot have more than one access config"
                )

    # validate no network interfaces were deleted
    for existing_network_interface in existing_network_interfaces:
        if existing_network_interface.get("name") not in changed_interfaces:
            result["result"] = False
            result["comment"].append(
                f"Network interface deletion not supported for interface {existing_network_interface.get('name')}"
            )

    # validation found errors
    if not result["result"]:
        return result

    for changed_interface_name, changed_interface_value in changed_interfaces.items():
        existing_network_interface = changed_interface_value.get("existing")
        new_network_interface = changed_interface_value.get("new")
        # According to documentation, only one access config per instance is supported.
        existing_access_configs = existing_network_interface.get("access_configs", [])
        # None or [] values should be differentiated
        desired_access_configs = new_network_interface.get("access_configs")

        if desired_access_configs is None:
            access_config_changes = {}
        else:
            access_config_changes = hub.tool.gcp.utils.compare_states(
                {"network_interfaces": [{"access_configs": existing_access_configs}]},
                {"network_interfaces": [{"access_configs": desired_access_configs}]},
                "compute.instance",
            )

        if access_config_changes:
            access_config_result = (
                await hub.tool.gcp.compute.instance.update_access_configs(
                    ctx,
                    existing_access_configs,
                    desired_access_configs,
                    current_instance.get("resource_id"),
                    changed_interface_name,
                )
            )
            if not access_config_result["result"]:
                result["result"] = False
                result["comment"] += access_config_result["comment"]
                return result

        # Network interface update
        # Cannot update access config through network interface update function - must be a separate call
        new_network_interface = hub.tool.gcp.utils.create_dict_body_on_top_of_old(
            existing_network_interface, new_network_interface
        )

        # We want to exclude access configs from update nic operation because it is not supported and
        # it is handled separately.
        new_network_interface.pop("access_configs", None)
        existing_network_interface = copy.copy(existing_network_interface)
        existing_network_interface.pop("access_configs", None)

        changes = hub.tool.gcp.utils.compare_states(
            {"network_interfaces": [existing_network_interface]},
            {"network_interfaces": [new_network_interface]},
            "compute.instance",
            additional_exclude_paths=["network_interfaces[].access_configs"],
        )

        if changes:
            if access_config_changes:
                get_ret = await hub.exec.gcp.compute.instance.get(
                    ctx, resource_id=current_instance.get("resource_id")
                )
                if not get_ret["result"] or not get_ret["ret"]:
                    result["result"] = False
                    result["comment"] += get_ret["comment"]
                    return result
                updated_network_interfaces = get_ret["ret"].get("network_interfaces")
                new_fingerprint = next(
                    (
                        updated_interface.get("fingerprint")
                        for updated_interface in updated_network_interfaces
                        if updated_interface.get("name") == changed_interface_name
                    ),
                    None,
                )
                new_network_interface["fingerprint"] = new_fingerprint
            op_ret = (
                await hub.exec.gcp_api.client.compute.instance.updateNetworkInterface(
                    ctx,
                    resource_id=current_instance.get("resource_id"),
                    network_interface=changed_interface_name,
                    body=new_network_interface,
                )
            )

            ret = await hub.tool.gcp.operation_utils.await_operation_completion(
                ctx, op_ret, "compute.instance", "compute.zone_operation"
            )
            if not ret["result"]:
                result["result"] = False
                result["comment"] += ret["comment"]
                return result

    result["result"] = True
    return result


async def update_access_configs(
    hub,
    ctx,
    existing_access_configs,
    desired_access_configs,
    instance_resource_id,
    network_interface_name,
) -> Dict[str, Any]:
    result = {"result": True, "comment": []}

    # it could still be [] and then desired_ac would be None
    if desired_access_configs is None:
        return result

    existing_ac = next(iter(existing_access_configs), None)
    desired_ac = next(iter(desired_access_configs), None)

    if not existing_ac and not desired_ac:
        return result

    if (
        existing_ac
        and not desired_ac
        or (
            existing_ac
            and desired_ac
            and desired_ac.get("nat_ip")
            and existing_ac.get("nat_ip") != desired_ac.get("nat_ip")
        )
    ):
        # See https://cloud.google.com/compute/docs/ip-addresses/reserve-static-external-ip-address#api_2
        # changing the external IP address of a VM requires deleting the existing access config first
        # and then adding a new one with the new IP
        op_ret = await hub.exec.gcp_api.client.compute.instance.deleteAccessConfig(
            ctx,
            resource_id=instance_resource_id,
            access_config=existing_ac.get("name"),
            network_interface=network_interface_name,
        )

        r = await hub.tool.gcp.operation_utils.await_operation_completion(
            ctx, op_ret, "compute.instance", "compute.zone_operation"
        )
        if not r["result"]:
            result["result"] = False
            result["comment"] += r["comment"]
            return result
        if existing_ac and not desired_ac:
            return result

    if (
        desired_ac
        and not existing_ac
        or (
            existing_ac
            and desired_ac
            and desired_ac.get("nat_ip")
            and existing_ac.get("nat_ip") != desired_ac.get("nat_ip")
        )
    ):
        # See https://cloud.google.com/compute/docs/ip-addresses/reserve-static-external-ip-address#api_2
        # changing the external IP address of a VM requires deleting the existing access config first
        # and then adding a new one with the new IP:
        op_ret = await hub.exec.gcp_api.client.compute.instance.addAccessConfig(
            ctx,
            resource_id=instance_resource_id,
            network_interface=network_interface_name,
            body=desired_ac,
        )

        r = await hub.tool.gcp.operation_utils.await_operation_completion(
            ctx, op_ret, "compute.instance", "compute.zone_operation"
        )
        if not r["result"]:
            result["result"] = False
            result["comment"] += r["comment"]

        return result

    # existing_ac and desired_ac and existing_ac.get("nat_ip") == desired_ac.get("nat_ip"))
    op_ret = await hub.exec.gcp_api.client.compute.instance.updateAccessConfig(
        ctx,
        resource_id=instance_resource_id,
        network_interface=network_interface_name,
        body=desired_ac,
    )

    r = await hub.tool.gcp.operation_utils.await_operation_completion(
        ctx, op_ret, "compute.instance", "compute.zone_operation"
    )
    if not r["result"]:
        result["result"] = False
        result["comment"] += r["comment"]

    return result


async def update_shielded_instance_config(
    hub,
    ctx,
    shielded_instance_config: Dict[str, bool],
    project: str = None,
    zone: str = None,
    instance: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    return await hub.exec.gcp.compute.instance.update_shielded_instance_config(
        ctx,
        shielded_instance_config["enable_secure_boot"],
        shielded_instance_config["enable_vtpm"],
        shielded_instance_config["enable_integrity_monitoring"],
        project,
        zone,
        instance,
        resource_id,
    )


async def update_shielded_instance_integrity_policy(
    hub,
    ctx,
    shielded_instance_integrity_policy: Dict[str, bool],
    project: str = None,
    zone: str = None,
    instance: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    return await hub.exec.gcp.compute.instance.set_shielded_instance_integrity_policy(
        ctx,
        shielded_instance_integrity_policy["update_auto_learn_policy"],
        project,
        zone,
        instance,
        resource_id,
    )


async def update_status(
    hub,
    ctx,
    resource_id: str,
    current_status: str,
    desired_status: str,
) -> Dict[str, Any]:
    result = {"result": False, "ret": None, "comment": []}

    states = ["RUNNING", "SUSPENDED", "TERMINATED"]
    if not desired_status in states:
        result["comment"].append(
            f"Incorrect instance status in the request: {desired_status}, must be one of: {states}"
        )
        return result

    # See https://cloud.google.com/compute/docs/instances/instance-life-cycle for instance's state transition diagram

    ret = None
    if current_status in ["PROVISIONING", "STAGING", "RUNNING", "REPAIRING"]:
        if desired_status == "TERMINATED":
            ret = await hub.exec.gcp.compute.instance.stop(ctx, resource_id=resource_id)
        elif desired_status == "SUSPENDED":
            ret = await hub.exec.gcp.compute.instance.suspend(
                ctx, resource_id=resource_id
            )
    elif current_status in ["STOPPING", "TERMINATED"] and desired_status == "RUNNING":
        ret = await hub.exec.gcp.compute.instance.start(ctx, resource_id=resource_id)
    elif current_status in ["SUSPENDING", "SUSPENDED"] and desired_status == "RUNNING":
        ret = await hub.exec.gcp.compute.instance.resume(ctx, resource_id=resource_id)
    else:
        result["comment"].append(
            f"Incorrect instance status transition: {current_status} => {desired_status}"
        )
        return result

    result["result"] = ret["result"]
    result["ret"] = ret["ret"]
    result["comment"] += ret["comment"]
    return result


async def on_completion(
    hub,
    ctx,
    completion_result: Dict,
    aux_ctx: Dict,
) -> Dict[str, Any]:
    old_state: Dict[str, Any] = completion_result["old_state"]
    new_state: Dict[str, Any] = completion_result["new_state"]

    if old_state:
        # Update operation
        return {}

    # Create operation completed -> enforce instance's runtime state
    if not aux_ctx or not aux_ctx.get("status"):
        return {}

    desired_status = aux_ctx.get("status")
    current_status = new_state.get("status")
    if desired_status == current_status:
        return {}

    result = await hub.tool.gcp.compute.instance.update_status(
        ctx, new_state.get("resource_id"), current_status, desired_status
    )
    if result["result"]:
        completion_result["new_state"] = result["ret"]

    return result
