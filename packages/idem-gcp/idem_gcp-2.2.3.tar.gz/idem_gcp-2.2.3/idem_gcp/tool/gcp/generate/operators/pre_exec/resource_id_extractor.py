from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext
from idem_gcp.tool.gcp.generate.exec_param import ExecParam


async def should_operate(hub, execution_context: ExecutionContext) -> bool:
    return (
        execution_context.get_exec_param_value(ExecParam.PROCESS_RESOURCE_ID_PARAM)
        and execution_context.get_method_param_value("resource_id") is not None
    )


async def operate(hub, execution_context: ExecutionContext) -> None:
    extended_params = {**execution_context.method_params}
    resource_id = extended_params.pop("resource_id", None)
    if resource_id is not None:
        resource_id_params = (
            hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
                execution_context.resource_type, resource_id
            )
        )
        aliases = execution_context.exec_params[ExecParam.PATH_PARAM_ALIASES]
        if not aliases:
            extended_params.update(resource_id_params)
        else:
            for resource_id_param in resource_id_params:
                if resource_id_param in aliases:
                    extended_params[aliases[resource_id_param]] = resource_id_params[
                        resource_id_param
                    ]

    execution_context.method_params = extended_params
