import asyncio
from typing import Any
from typing import Dict


async def handle_operation(
    hub, ctx, rerun_data, resource_type: str, wait_until_done: bool = False
) -> Dict[str, Any]:
    result = {
        "comment": [],
        "result": True,
        "rerun_data": None,
        "resource_id": None,
    }

    operation_id = rerun_data.get("operation_id")
    operation_type = hub.tool.gcp.operation_utils.get_operation_type(operation_id)

    if operation_type is None:
        result["result"] = False
        result["comment"].append(
            f"Cannot determine operation scope (zonal/regional/global) {operation_id}"
        )
        result["rerun_data"] = {"has_error": True}
        return result

    if operation_type == "compute.zone_operation":
        get_ret = await hub.exec.gcp_api.client.compute.zone_operation.get(
            ctx, resource_id=operation_id
        )
    elif operation_type == "compute.region_operation":
        get_ret = await hub.exec.gcp_api.client.compute.region_operation.get(
            ctx, resource_id=operation_id
        )
    elif operation_type == "compute.global_operation":
        get_ret = await hub.exec.gcp_api.client.compute.global_operation.get(
            ctx, resource_id=operation_id
        )

    if not get_ret["result"] or not get_ret["ret"]:
        result["result"] = False
        result["comment"] = get_ret["comment"]
        result["rerun_data"] = {"has_error": True}
        return result

    operation = get_ret["ret"]
    op_ret = {}
    if operation["status"] != "DONE":
        if wait_until_done:
            op_ret = await hub.tool.gcp.operation_utils.wait_for_operation(
                ctx, operation, operation_type
            )
            operation = op_ret["ret"]
        else:
            result["result"] = False
            new_operation_id = (
                hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                    operation.get("selfLink"), operation_type
                )
            )
            rerun_data["operation_id"] = new_operation_id
            result["rerun_data"] = rerun_data

            result["comment"] += get_ret["comment"]
            return result

    op_ret_error_comments = [
        comment for comment in op_ret.get("comment", []) if "errors" in comment
    ]
    if (operation and operation.get("error")) or op_ret_error_comments:
        result["result"] = False
        if operation:
            result["comment"].append(str(operation.get("error", {})))

        result["comment"] += op_ret_error_comments
        result["rerun_data"] = {"has_error": True}
        return result

    result["resource_id"] = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
        operation.get("targetLink"), resource_type
    )

    return result


async def wait_for_operation(hub, ctx, operation, operation_type: str) -> Dict:
    max_timeout_retries = 5
    timeout_retries = 0
    while True:
        if operation_type == "compute.zone_operation":
            op_ret = await hub.exec.gcp_api.client.compute.zone_operation.wait(
                ctx, resource_id=operation["selfLink"]
            )
        elif operation_type == "compute.region_operation":
            op_ret = await hub.exec.gcp_api.client.compute.region_operation.wait(
                ctx, resource_id=operation["selfLink"]
            )
        elif operation_type == "compute.global_operation":
            op_ret = await hub.exec.gcp_api.client.compute.global_operation.wait(
                ctx, resource_id=operation["selfLink"]
            )

        if not op_ret or not op_ret["ret"] or not op_ret["result"]:
            if timeout_retries < max_timeout_retries:
                timeout_retries += 1
                continue
            else:
                break

        operation = op_ret["ret"]
        op_ret_error_comments = [
            comment for comment in op_ret["comment"] if "errors" in comment
        ]
        if (
            operation["status"] == "DONE"
            or "error" in operation
            or op_ret_error_comments
        ):
            break

        await asyncio.sleep(1)

    return op_ret


def get_operation_type(hub, operation_id) -> str:
    if not operation_id:
        return None
    if "/zones/" in operation_id:
        return "compute.zone_operation"
    elif "/regions/" in operation_id:
        return "compute.region_operation"
    elif "/global/" in operation_id:
        return "compute.global_operation"
    else:
        return None


async def await_operation_completion(
    hub, ctx, api_call_ret: Dict[str, Any], resource_type: str, operation_type: str
) -> Dict[str, Any]:
    result = {"result": False, "comment": []}

    if not api_call_ret["result"] and not api_call_ret["ret"]:
        result["comment"] += api_call_ret["comment"]
        return result

    if hub.tool.gcp.operation_utils.is_operation(api_call_ret["ret"]):
        operation = api_call_ret["ret"]

        operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            operation.get("selfLink"), operation_type
        )
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            ctx, {"operation_id": operation_id}, resource_type, True
        )

        if not handle_operation_ret["result"]:
            result["comment"] += handle_operation_ret["comment"]
            return result

    result["result"] = True
    return result


def is_operation(hub, candidate) -> bool:
    return (
        candidate and "kind" in candidate and candidate["kind"].endswith("#operation")
    )
