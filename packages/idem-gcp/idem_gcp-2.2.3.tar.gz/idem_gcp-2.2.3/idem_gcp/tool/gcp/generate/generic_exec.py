from typing import Any
from typing import Dict

from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext


def __init__(hub):
    hub.tool.gcp.generate.PRE_EXECS_ORDER = [
        "resource_id_extractor",
        "parameter_sanitizer",
        "function_getter",
    ]
    hub.tool.gcp.generate.POST_EXECS_ORDER = ["operation_processor", "item_getter"]


async def execute(hub, execution_context: ExecutionContext) -> Dict[str, Any]:
    for operator_name in hub.tool.gcp.generate.PRE_EXECS_ORDER:
        operator = hub.tool.gcp.generate.generic_exec.get_pre_exec_operator(
            operator_name
        )
        if await operator.should_operate(execution_context):
            try:
                await operator.operate(execution_context)
            except ValueError as e:
                return {"result": False, "ret": None, "comment": [str(e)]}

    execution_context.response = await execution_context.method(
        **execution_context.method_params
    )

    for operator_name in hub.tool.gcp.generate.POST_EXECS_ORDER:
        operator = hub.tool.gcp.generate.generic_exec.get_post_exec_operator(
            operator_name
        )
        if await operator.should_operate(execution_context):
            await operator.operate(execution_context)

    return execution_context.response


def get_pre_exec_operator(hub, name: str):
    return getattr(hub.tool.gcp.generate.operators.pre_exec, name)


def get_post_exec_operator(hub, name: str):
    return getattr(hub.tool.gcp.generate.operators.post_exec, name)
