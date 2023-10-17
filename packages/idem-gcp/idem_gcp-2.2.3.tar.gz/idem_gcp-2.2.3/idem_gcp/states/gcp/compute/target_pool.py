"""State module for managing Target Pool."""
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    region: str = None,
    project: str = None,
    instances: List[str] = None,
    session_affinity: str = None,
    description: str = None,
    failover_ratio: float = None,
    health_checks: List[str] = None,
    backup_pool: str = None,
    request_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Creates a target pool in the specified project and region using the data included in the request.

    Args:
        name(str):
            An Idem name of the resource.
        instances(List[str], Optional):
            A list of resource URLs to the virtual machine instances serving this pool. They must live in zones contained in the same region as this pool. Defaults to None.
        session_affinity(str, Optional):
            Session affinity option, must be one of the following values:
            NONE: Connections from the same client IP may go to any instance in the pool.
            CLIENT_IP: Connections from the same client IP will go to the same instance in the pool while that instance remains healthy.
            CLIENT_IP_PROTO: Connections from the same client IP with the same IP protocol will go to the same instance in the pool while that instance remains healthy.
        description(str, Optional):
            An optional description of this resource. Provide this property when you create the resource. Defaults to None.
        region(str, Optional):
            Name of the region scoping this request.
        failover_ratio(float, Optional):
            This field is applicable only when the containing target pool is serving a forwarding rule as the primary pool (i.e., not as a backup pool to some other target pool). The value of the field must be in [0, 1]. If set, backupPool must also be set. They together define the fallback behavior of the primary target pool: if the ratio of the healthy instances in the primary pool is at or below this number, traffic arriving at the load-balanced IP will be directed to the backup pool. In case where failoverRatio is not set or all the instances in the backup pool are unhealthy, the traffic will be directed back to the primary pool in the "force" mode, where traffic will be spread to the healthy instances with the best effort, or to all instances when no instance is healthy. Defaults to None.
        health_checks(List[str], Optional):
            The URL of the HttpHealthCheck resource. A member instance in this pool is considered healthy if and only if the health checks pass. Only legacy HttpHealthChecks are supported. Only one health check may be specified. Defaults to None.
        backup_pool(str, Optional):
            The server-defined URL for the resource. This field is applicable only when the containing target pool is serving a forwarding rule as the primary pool, and its failoverRatio field is properly set to a value between [0, 1]. backupPool and failoverRatio together define the fallback behavior of the primary target pool: if the ratio of the healthy instances in the primary pool is at or below failoverRatio, traffic arriving at the load-balanced IP will be directed to the backup pool. In case where failoverRatio and backupPool are not set, or all the instances in the backup pool are unhealthy, the traffic will be directed back to the primary pool in the "force" mode, where traffic will be spread to the healthy instances with the best effort, or to all instances when no instance is healthy. Defaults to None.
        project(str, Optional):
            Project ID for this request.
        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.
        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              gcp.compute.target_pool.present:
                - name: value
                - region: value
                - project: value
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    # TODO uncomment below line, when implementation is added
    # project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    result["comment"].append(
        hub.tool.gcp.comment_utils.no_resource_create_update_comment(
            "gcp.compute.target_pool"
        )
    )

    return result


async def absent(
    hub,
    ctx,
    name: str,
    project: str = None,
    region: str = None,
    request_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Deletes the specified target pool.

    Args:
        name(str):
            An Idem name of the resource.

        project(str, Optional):
            Project ID for this request.

        region(str, Optional):
            Name of the region scoping this request.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              gcp.compute.target_pool.absent:
                - name: value
                - project: value
                - region: value
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    # TODO uncomment below line, when implementation is added
    # project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    result["comment"].append(
        hub.tool.gcp.comment_utils.no_resource_delete_comment("gcp.compute.target_pool")
    )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves a list of target pools available to the specified project and region.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.target_pool
    """
    result = {}

    # TODO: Pagination
    describe_ret = await hub.exec.gcp.compute.target_pool.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(
            f"Could not describe gcp.compute.target_pool {describe_ret['comment']}"
        )
        return {}

    for resource in describe_ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "gcp.compute.target_pool.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
