"""Exec module for managing Target Pool."""

__func_alias__ = {"list_": "list"}

from typing import Any, Dict

from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext
from idem_gcp.tool.gcp.generate.exec_param import ExecParam
from idem_gcp.tool.gcp.generate.scope import Scope


async def list_(
    hub,
    ctx,
    project: str = None,
    region: str = None,
    filter_: (str, "alias=filter") = None,
    order_by: str = None,
):
    r"""Retrieves a list of target pools available to the specified project and region.

    Args:
        project(str, Optional):
            Project ID for this request.

        region(str, Optional):
            Name of the region scoping this request.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = \"Intel Skylake\") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = \"Intel Skylake\") OR (cpuPlatform = \"Intel Broadwell\") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq \"double quoted literal\"` `(fieldname1 eq literal) (fieldname2 ne \"literal\")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name "instance", you would use `name ne .*instance`.

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy=\"creationTimestamp desc\"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported.

    Examples:
        .. code-block:: sls

            list-target_pool:
              exec.run:
              - path: gcp.compute.target_pool.list
              - kwargs:
                  project: project-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type="compute.target_pool",
        method_name="list",
        method_params={
            "ctx": ctx,
            "project": project,
            "region": region,
            "filter": filter_,
            "order_by": order_by,
        },
        exec_params={
            ExecParam.SCOPED_FUNCTIONS: {
                Scope.REGIONAL: "list",
                Scope.GLOBAL: "aggregatedList",
            }
        },
    )

    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def get(
    hub,
    ctx,
    project: str = None,
    region: str = None,
    name: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Returns the specified target pool.

    Args:
        project (str, Optional):
            Project ID for this request.
        region (str, Optional):
            The region in which to search.
        name (str, Optional):
            Name of the TargetPool resource to return.
        resource_id (str, Optional):
            Idem resource ID.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            get-target-pool:
                exec.run:
                   - path: gcp.compute.target_pool.get
                   - kwargs:
                       project: project-name
                       name: target-pool-name
                       region: region-name
                       resource_id: resource-id
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type="compute.target_pool",
        method_name="get",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "region": region,
            "targetPool": name,
        },
    )

    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)
