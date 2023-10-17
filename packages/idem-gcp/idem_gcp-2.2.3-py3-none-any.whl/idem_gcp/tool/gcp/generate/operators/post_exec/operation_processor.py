from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext


async def should_operate(hub, execution_context: ExecutionContext) -> bool:
    return (
        execution_context.response is not None
        and execution_context.response.get("ret") is not None
        and hub.tool.gcp.operation_utils.is_operation(execution_context.response["ret"])
    )


async def operate(hub, execution_context: ExecutionContext) -> None:
    execution_context.response["result"] = True
    operation = execution_context.response["ret"]
    operation_type = hub.tool.gcp.generate.operators.post_exec.operation_processor.get_operation_type(
        operation
    )
    if operation_type is None:
        execution_context.response["result"] = False
        execution_context.response["comment"].append(
            "Unexpected operation type returned"
        )
        return
    operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
        operation.get("selfLink"), operation_type
    )
    handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
        execution_context.method_params.get("ctx"),
        {"operation_id": operation_id},
        execution_context.resource_type,
        wait_until_done=True,
    )

    if not handle_operation_ret["result"]:
        execution_context.response["result"] = False
        execution_context.response["comment"] += handle_operation_ret["comment"]

    # if op_ret["result"] is True, then the operation is finished and resource_id is returned,
    # even if op_ret["result"] is False, we still need to get the actual state of the resource
    resource_id = handle_operation_ret.get("resource_id") or (
        hub.tool.gcp.resource_prop_utils.construct_resource_id(
            execution_context.resource_type, execution_context.method_params
        )
    )
    resource_get_result = await hub.tool.gcp.generate.operators.post_exec.operation_processor.invoke_get_operation_for_resource(
        execution_context, resource_id
    )

    if resource_get_result is None:
        execution_context.response["result"] = False
        execution_context.response["comment"].append("Could not find resource")
        return

    execution_context.response["ret"] = resource_get_result["ret"]

    if not resource_get_result["result"]:
        execution_context.response["result"] = False
        execution_context.response["comment"] += resource_get_result["comment"]
        return


def get_operation_type(hub, operation) -> str:
    return hub.tool.gcp.operation_utils.get_operation_type(operation.get("selfLink"))


async def invoke_get_operation_for_resource(hub, execution_context, resource_id):
    resource_type = execution_context.resource_type
    resource_path = resource_type.split(".")
    hub_ref = hub.exec.gcp
    for resource_path_segment in resource_path:
        hub_ref = hub_ref[resource_path_segment]
    ctx = execution_context.method_params.get("ctx")
    return await hub_ref.get(ctx, resource_id=resource_id)
