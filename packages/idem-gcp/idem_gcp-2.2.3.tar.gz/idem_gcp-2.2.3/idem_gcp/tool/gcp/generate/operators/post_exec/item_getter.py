from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext
from idem_gcp.tool.gcp.generate.exec_param import ExecParam


async def should_operate(hub, execution_context: ExecutionContext) -> bool:
    return (
        execution_context.get_exec_param_value(ExecParam.GET_ITEMS)
        and "list" in execution_context.method_name.lower()
        and execution_context.response.get("ret") is not None
        and "items" in execution_context.response.get("ret")
    )


async def operate(hub, execution_context: ExecutionContext) -> None:
    response = execution_context.response
    execution_context.response = {
        **response,
        "ret": response.get("ret").get("items", []),
    }
