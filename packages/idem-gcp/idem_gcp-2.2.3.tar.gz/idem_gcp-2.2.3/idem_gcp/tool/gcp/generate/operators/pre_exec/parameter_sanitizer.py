from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext
from idem_gcp.tool.gcp.generate.exec_param import ExecParam


async def should_operate(hub, execution_context: ExecutionContext) -> bool:
    return execution_context.get_exec_param_value(ExecParam.SANITIZE_PARAM)


async def operate(hub, execution_context: ExecutionContext) -> None:
    sanitized_params = {
        k: v for k, v in execution_context.method_params.items() if v is not None
    }
    execution_context.method_params = sanitized_params
