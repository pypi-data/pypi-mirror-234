from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext
from idem_gcp.tool.gcp.generate.exec_param import ExecParam
from idem_gcp.tool.gcp.generate.scope import Scope


async def should_operate(hub, execution_context: ExecutionContext) -> bool:
    return True


async def operate(hub, execution_context: ExecutionContext) -> None:
    if execution_context.get_exec_param_value(ExecParam.SCOPED_FUNCTIONS) is not None:
        _find_scoped_method_name(execution_context)
    execution_context.method = hub.tool.gcp.resolver.resolve_sub(
        ".".join(
            ["gcp", execution_context.resource_type, execution_context.method_name]
        ),
        hub.tool.gcp.API,
    )


# modifies method_name to use appropriate one for scope
# removes redundant scope-related method parameters
def _find_scoped_method_name(execution_context: ExecutionContext):
    method_params = execution_context.method_params
    scope = Scope.GLOBAL
    if method_params.get("zone") is not None:
        scope = Scope.ZONAL
    else:
        # remove zone from method params, as it is not expected from non-zonal methods
        method_params.pop("zone", None)

    if method_params.get("region") is not None:
        scope = Scope.REGIONAL
    else:
        method_params.pop("region", None)

    scoped_functions = execution_context.get_exec_param_value(
        ExecParam.SCOPED_FUNCTIONS
    )

    if scoped_functions is not None and scoped_functions.get(scope) is not None:
        execution_context.method_name = scoped_functions.get(scope)
