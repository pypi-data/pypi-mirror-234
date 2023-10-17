"""Exec module for managing Networks."""
from typing import Any
from typing import Dict

from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext

__func_alias__ = {"list_": "list"}


async def list_(
    hub,
    ctx,
    project: str = None,
    filter_: (str, "alias=filter") = None,
    max_results: int = 500,
    order_by: str = None,
    page_token: str = None,
    return_partial_success: bool = False,
) -> Dict[str, Any]:
    r"""Retrieves the list of networks available to the specified project.

    Args:
        project(str, Optional):
            Project ID for this request.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = \"Intel Skylake\") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = \"Intel Skylake\") OR (cpuPlatform = \"Intel Broadwell\") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq \"double quoted literal\"` `(fieldname1 eq literal) (fieldname2 ne \"literal\")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name "instance", you would use `name ne .*instance`.

        max_results(int, Optional):
            The maximum number of results per page that should be returned. If the number of available results is larger than `maxResults`, Compute Engine returns a `nextPageToken` that can be used to get the next page of results in subsequent list requests. Acceptable values are `0` to `500`, inclusive. (Default: `500`)

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy=\"creationTimestamp desc\"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported.

        page_token(str, Optional):
            Specifies a page token to use. Set `pageToken` to the `nextPageToken` returned by a previous list request to get the next page of results.

        return_partial_success(bool, Optional):
            Opt-in for partial success behavior which provides partial results in case of failure. The default value is false.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.network.list
              - kwargs:
                  project: project-name
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    ret = await hub.exec.gcp_api.client.compute.network.list(
        ctx,
        project=project,
        filter=filter_,
        maxResults=max_results,
        orderBy=order_by,
        pageToken=page_token,
        returnPartialSuccess=return_partial_success,
    )

    if not ret["result"]:
        result["comment"] += ret["comment"]
        result["result"] = False
        return result

    result["ret"] = ret["ret"].get("items", [])
    return result


async def get(
    hub, ctx, resource_id: str = None, project: str = None, name: str = None
) -> Dict[str, Any]:
    r"""Returns the specified network. Gets a list of available networks by making a list() request.

    Args:
        resource_id(str, Optional):
            An identifier of the resource in the provider.

        project(str, Optional):
            Project ID for this request.

        name(str, Optional):
            Name of the network to return.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.network.get
              - kwargs:
                  project: project-name
                  name: network-name
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    if resource_id:
        ret = await hub.exec.gcp_api.client.compute.network.get(
            ctx, resource_id=resource_id
        )
    elif project and name:
        ret = await hub.exec.gcp_api.client.compute.network.get(
            ctx, project=project, network=name
        )
    else:
        result["result"] = False
        result["comment"] = [
            f"gcp.compute.network#get(): {name} either resource_id or project and network should be specified."
        ]
        return result

    if not ret["result"]:
        result["comment"] += ret["comment"]
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result


async def get_effective_firewalls(
    hub,
    ctx,
    project: str = None,
    network: str = None,
    resource_id: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""Returns the effective firewalls on a given network.

    Args:
        network(str):
            Name of the network for this request.

        project(str, Optional):
            Project ID for this request. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).  Defaults to None.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.network.get_effective_firewalls
              - kwargs:
                  project: project-name
                  network: network-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type="compute.network",
        method_name="getEffectiveFirewalls",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "network": network,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def list_peering_routes(
    hub,
    ctx,
    peering_name: str,
    region: str,
    direction: str,
    network: str = None,
    resource_id: str = None,
    project: str = None,
    filter_: (str, "alias=filter") = None,
    order_by: str = None,
) -> Dict[str, Any]:
    r"""Lists the peering routes exchanged over peering connection.

    Args:
        peering_name(str):
            The response will show routes exchanged over the given peering connection.

        direction(str):
            The direction of the exchanged routes.
                Enum type. Allowed values:
                "INCOMING" - For routes exported from peer network.
                "OUTGOING" - For routes exported from local network.

        region(str):
            The region of the request. The response will include all subnet routes, static routes and dynamic routes in the region.

        project(str, Optional):
            Project ID for this request.

        network(str, Optional):
            Name of the network for this request.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = \"Intel Skylake\") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = \"Intel Skylake\") OR (cpuPlatform = \"Intel Broadwell\") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq \"double quoted literal\"` `(fieldname1 eq literal) (fieldname2 ne \"literal\")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name "instance", you would use `name ne .*instance`.

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy=\"creationTimestamp desc\"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.network.list_peering_routes
              - kwargs:
                  project: project-name
                  region: region-name
                  network: network-name
                  direction: direction-name
                  peering_name: peering-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    # GCP method name is simply the name of this func or the one from __func_alias - we can pass it
    # also we can pass the resource name based on the file name
    execution_context = ExecutionContext(
        resource_type="compute.network",
        method_name="listPeeringRoutes",
        method_params={
            "ctx": ctx,
            "network": network,
            "peering_name": peering_name,
            "region": region,
            "direction": direction,
            "resource_id": resource_id,
            "project": project,
            "filter": filter_,
            "order_by": order_by,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def switch_to_custom_mode(
    hub,
    ctx,
    project: str = None,
    network: str = None,
    resource_id: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""Switches the network mode from auto subnet mode to custom subnet mode.

    Args:
        network(str, Optional):
            Name of the network to be updated.

        project(str, Optional):
            Project ID for this request. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).  Defaults to None.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.network.switch_to_custom_mode
              - kwargs:
                  project: project-name
                  network: network-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type="compute.network",
        method_name="switchToCustomMode",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "network": network,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)
