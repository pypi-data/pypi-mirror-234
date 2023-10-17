from typing import Any
from typing import Dict
from typing import List


async def update_size_gb(
    hub,
    ctx,
    current_size_gb: str,
    desired_size_gb: str,
    resource_id: str,
    request_id: str,
) -> Dict[str, Any]:
    result = {"result": True, "comment": []}

    if desired_size_gb is not None and str(current_size_gb) != str(desired_size_gb):
        if not ctx.get("test"):
            resize_body = {"size_gb": desired_size_gb}
            update_ret = await hub.exec.gcp_api.client.compute.disk.resize(
                ctx,
                resource_id=resource_id,
                body=resize_body,
                request_id=request_id,
            )

            if not update_ret["result"]:
                result["result"] = False
                result["comment"] += update_ret["comment"]
                return result

            if hub.tool.gcp.operation_utils.is_operation(update_ret["ret"]):
                operation = update_ret["ret"]
                operation_type = hub.tool.gcp.operation_utils.get_operation_type(
                    operation.get("selfLink")
                )
                operation_id = (
                    hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                        operation.get("selfLink"), operation_type
                    )
                )
                handle_operation_ret = (
                    await hub.tool.gcp.operation_utils.handle_operation(
                        ctx,
                        {"operation_id": operation_id},
                        "compute.disk",
                        True,
                    )
                )
                if not handle_operation_ret["result"]:
                    result["result"] = False
                    result["comment"] += handle_operation_ret["comment"]
                    return result

    return result


async def update_labels(
    hub,
    ctx,
    current_labels: Dict[str, str],
    new_labels: Dict[str, str],
    label_fingerprint: str,
    request_id: str,
    project: str,
    name: str,
    zone: str,
    region: str,
) -> Dict[str, Any]:
    result = {"result": True, "comment": []}

    if (
        new_labels is not None
        and not (new_labels == {} and current_labels is None)
        and current_labels != new_labels
    ):
        if not ctx.get("test"):
            set_labels_body = {
                "labels": new_labels,
                "label_fingerprint": label_fingerprint,
            }
            kwargs = {
                "project": project,
                "resource": name,
                "body": set_labels_body,
                "request_id": request_id,
            }
            if zone:
                kwargs.update({"zone": zone})
            if region:
                kwargs.update({"region": region})

            update_ret = await hub.exec.gcp_api.client.compute.disk.setLabels(
                ctx,
                **kwargs,
            )

            if not update_ret["result"]:
                result["result"] = False
                result["comment"] += update_ret["comment"]
                return result

            if hub.tool.gcp.operation_utils.is_operation(update_ret["ret"]):
                operation = update_ret["ret"]
                operation_type = hub.tool.gcp.operation_utils.get_operation_type(
                    operation.get("selfLink")
                )
                operation_id = (
                    hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                        operation.get("selfLink"), operation_type
                    )
                )
                handle_operation_ret = (
                    await hub.tool.gcp.operation_utils.handle_operation(
                        ctx,
                        {"operation_id": operation_id},
                        "compute.disk",
                        True,
                    )
                )
                if not handle_operation_ret["result"]:
                    result["result"] = False
                    result["comment"] += handle_operation_ret["comment"]
                    return result

    return result


async def update_resource_policies(
    hub,
    ctx,
    current_resource_policies: List[str],
    desired_resource_policies: List[str],
    resource_id: str,
    request_id: str,
) -> Dict[str, Any]:
    result = {"result": True, "comment": []}

    if not hub.tool.gcp.state_comparison_utils.are_lists_identical(
        current_resource_policies, desired_resource_policies
    ):
        # If (some) resource policies are links, parse them to resource policy resource ids
        new_resource_policies = [
            hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                policy, "compute.resource_policy"
            )
            for policy in (
                desired_resource_policies
                if desired_resource_policies is not None
                else []
            )
        ]
        current_resource_policies = [
            hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                policy, "compute.resource_policy"
            )
            for policy in current_resource_policies or []
        ]

        resource_policies_to_remove = [
            policy
            for policy in current_resource_policies
            if policy not in new_resource_policies
        ]
        resource_policies_to_add = [
            policy
            for policy in new_resource_policies
            if policy not in current_resource_policies
        ]

        if len(resource_policies_to_remove) > 0 or len(resource_policies_to_add) > 0:
            if not ctx.get("test"):
                add_request_body = None
                if len(resource_policies_to_add) > 0:
                    add_request_body = {"resource_policies": resource_policies_to_add}
                remove_request_body = None
                if len(resource_policies_to_remove) > 0:
                    remove_request_body = {
                        "resource_policies": resource_policies_to_remove
                    }

                remove_ret = None
                if remove_request_body is not None:
                    remove_ret = await hub.exec.gcp_api.client.compute.disk.removeResourcePolicies(
                        ctx,
                        resource_id=resource_id,
                        body=remove_request_body,
                        request_id=request_id,
                    )

                    if not remove_ret["result"]:
                        result["result"] = False
                        result["comment"] += remove_ret["comment"]
                        return result

                    if hub.tool.gcp.operation_utils.is_operation(remove_ret["ret"]):
                        operation = remove_ret["ret"]
                        operation_type = (
                            hub.tool.gcp.operation_utils.get_operation_type(
                                operation.get("selfLink")
                            )
                        )
                        operation_id = (
                            hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                                operation.get("selfLink"), operation_type
                            )
                        )
                        handle_operation_ret = (
                            await hub.tool.gcp.operation_utils.handle_operation(
                                ctx,
                                {"operation_id": operation_id},
                                "compute.disk",
                                True,
                            )
                        )
                        if not handle_operation_ret["result"]:
                            result["result"] = False
                            result["comment"] += handle_operation_ret["comment"]
                            return result

                if (
                    remove_ret is None or remove_ret["result"]
                ) and add_request_body is not None:
                    add_ret = (
                        await hub.exec.gcp_api.client.compute.disk.addResourcePolicies(
                            ctx,
                            resource_id=resource_id,
                            body=add_request_body,
                            request_id=request_id,
                        )
                    )

                    if not add_ret["result"]:
                        result["result"] = False
                        result["comment"] += add_ret["comment"]
                        return result

                    if hub.tool.gcp.operation_utils.is_operation(add_ret["ret"]):
                        operation = add_ret["ret"]
                        operation_type = (
                            hub.tool.gcp.operation_utils.get_operation_type(
                                operation.get("selfLink")
                            )
                        )
                        operation_id = (
                            hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                                operation.get("selfLink"), operation_type
                            )
                        )
                        handle_operation_ret = (
                            await hub.tool.gcp.operation_utils.handle_operation(
                                ctx,
                                {"operation_id": operation_id},
                                "compute.disk",
                                True,
                            )
                        )
                        if not handle_operation_ret["result"]:
                            result["comment"] += handle_operation_ret["comment"]
                            return result

    return result
