import copy
from typing import Any
from typing import Dict
from typing import List


async def update_peerings(
    hub,
    ctx,
    resource_id: str,
    current_peerings: List[Dict[str, Any]],
    new_peerings: List[Dict[str, Any]],
) -> Dict[str, Any]:
    result = {"result": False, "comment": []}

    current_peerings = current_peerings if current_peerings is not None else []
    new_peerings = new_peerings if new_peerings is not None else []

    existing_peering_names = {
        peering.get("name"): peering for peering in current_peerings
    }
    new_peering_names = {peering.get("name"): peering for peering in new_peerings}

    peerings_to_add = []
    peerings_to_update = []

    for new_peering in new_peerings:
        if new_peering.get("name") not in existing_peering_names:
            peerings_to_add.append(new_peering)
        else:
            peering_changes = hub.tool.gcp.utils.compare_states(
                {"peering": new_peering},
                {
                    "peering": next(
                        current_peering
                        for current_peering in current_peerings
                        if current_peering.get("name") == new_peering.get("name")
                    )
                },
                resource_type=None,
                additional_exclude_paths=["auto_create_routes"],
            )

            if peering_changes:
                peerings_to_update.append(new_peering)

    peerings_to_remove = [
        peering
        for peering in current_peerings
        if peering.get("name") not in new_peering_names
    ]

    # Remove peerings
    for peering in peerings_to_remove:
        remove_peering_request_body = {"name": peering.get("name")}

        remove_ret = await hub.exec.gcp_api.client.compute.network.removePeering(
            ctx, resource_id=resource_id, body=remove_peering_request_body
        )

        r = await hub.tool.gcp.operation_utils.await_operation_completion(
            ctx, remove_ret, "compute.network", "compute.global_operation"
        )
        if not r["result"]:
            result["comment"] += r["comment"]
            return result

    # Update peerings
    for peering in peerings_to_update:
        # We want to remove this property, as it will soon be deprecated.
        # exchange_subnet_routes should be used instead.
        peering.pop("auto_create_routes", None)

        # Ignoring this property, until figuring out why get does not return it and how to update it.
        peering.pop("peer_mtu", None)

        update_peering_request_body = {"network_peering": peering}

        update_ret = await hub.exec.gcp_api.client.compute.network.updatePeering(
            ctx, resource_id=resource_id, body=update_peering_request_body
        )

        r = await hub.tool.gcp.operation_utils.await_operation_completion(
            ctx, update_ret, "compute.network", "compute.global_operation"
        )
        if not r["result"]:
            result["comment"] += r["comment"]
            return result

    # Add peerings
    r = await hub.tool.gcp.compute.network.add_peerings(
        ctx, resource_id, peerings_to_add
    )

    if not r["result"]:
        result["comment"] += r["comment"]
        return result

    result["result"] = True
    return result


async def add_peerings(
    hub, ctx, resource_id: str, peerings_to_add: Dict[str, Any]
) -> Dict[str, Any]:
    result = {"result": False, "comment": []}

    for peering in peerings_to_add:
        # We want to remove this property, as it will soon be deprecated.
        # exchange_subnet_routes should be used instead.
        peering.pop("auto_create_routes", None)

        add_peering_request_body = {"network_peering": peering}

        add_ret = await hub.exec.gcp_api.client.compute.network.addPeering(
            ctx, resource_id=resource_id, body=add_peering_request_body
        )

        r = await hub.tool.gcp.operation_utils.await_operation_completion(
            ctx, add_ret, "compute.network", "compute.global_operation"
        )
        if not r["result"]:
            result["comment"] += r["comment"]
            return result

    result["result"] = True
    return result


def build_new_peerings_on_top_of_old(
    hub, old_peerings: List[Dict[str, Any]], new_peerings: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    if new_peerings:
        new_peerings = copy.deepcopy(new_peerings)
        # Ignoring this property, until figuring out why get does not return it and how to update it.
        for peering in new_peerings:
            peering.pop("peer_mtu", None)
    if not new_peerings or not old_peerings:
        return new_peerings

    new_peerings = new_peerings or []
    old_peerings = old_peerings or []

    new_peerings_body = []
    for new_peering in new_peerings:
        old_peering = next(
            peering
            for peering in old_peerings
            if new_peering.get("name") == peering.get("name")
        )
        if old_peering:
            new_peering_body = hub.tool.gcp.utils.create_dict_body_on_top_of_old(
                old_peering, new_peering
            )
        else:
            new_peering_body = new_peering

        new_peerings_body.append(new_peering_body)

    return new_peerings_body
