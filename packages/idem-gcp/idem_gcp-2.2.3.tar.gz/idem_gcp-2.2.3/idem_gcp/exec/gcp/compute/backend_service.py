"""Exec module for managing Backend Services."""

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
    r"""Retrieves the list of Backend services available to the specified project.

    Args:
        project(str, Optional):
            Project ID for this request.

        region(str, Optional):
            The region in which to search. If not provided Backend services from all regions will be presented.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = \"Intel Skylake\") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = \"Intel Skylake\") OR (cpuPlatform = \"Intel Broadwell\") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq \"double quoted literal\"` `(fieldname1 eq literal) (fieldname2 ne \"literal\")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name "instance", you would use `name ne .*instance`.

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy=\"creationTimestamp desc\"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported.

    Examples:
        .. code-block:: sls

            list-backend_service:
              exec.run:
              - path: gcp.compute.backend_service.list
              - kwargs:
                  project: project-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    method_params = {
        "ctx": ctx,
        "project": project,
        "region": region,
        "filter": filter_,
        "orderBy": order_by,
    }

    if region:
        rt = "compute.region_backend_service"
    else:
        rt = "compute.backend_service"

    return await hub.tool.gcp.generate.generic_exec.execute(
        ExecutionContext(
            resource_type=rt,
            method_name="list",
            method_params=method_params,
            exec_params={
                ExecParam.SCOPED_FUNCTIONS: {
                    Scope.REGIONAL: "list",
                    Scope.GLOBAL: "aggregatedList",
                }
            },
        )
    )


async def get(
    hub,
    ctx,
    project: str = None,
    region: str = None,
    name: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Returns the specified global Backend service.

    Args:
        project: Project ID for this request.
        region(str, Optional):
            The region in which to search.
        name: Name of the global Backend service to return.
        resource_id: Idem resource ID.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            get-backend-service:
                exec.run:
                   - path: gcp.compute.backend_service.get
                   - kwargs:
                       project: project-name
                       name: backend-service-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    return await hub.tool.gcp.generate.generic_exec.execute(
        ExecutionContext(
            resource_type="compute.region_backend_service",
            method_name="get",
            method_params={
                "ctx": ctx,
                "resource_id": resource_id,
                "project": project,
                "region": region,
                "backendService": name,
            },
        )
    )
