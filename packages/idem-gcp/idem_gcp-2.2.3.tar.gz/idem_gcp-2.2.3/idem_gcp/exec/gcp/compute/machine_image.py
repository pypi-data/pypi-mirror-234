"""Exec module for managing Machine Images."""
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def list_(
    hub,
    ctx,
    project: str = None,
    filter_: (str, "alias=filter") = None,
    order_by: str = None,
) -> Dict[str, Any]:
    r"""Retrieves a list of machine images that are contained within the specified project.

    Args:
        project(str, Optional):
            Project ID for this request.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = \"Intel Skylake\") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = \"Intel Skylake\") OR (cpuPlatform = \"Intel Broadwell\") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq \"double quoted literal\"` `(fieldname1 eq literal) (fieldname2 ne \"literal\")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name "instance", you would use `name ne .*instance`.

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy=\"creationTimestamp desc\"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported.
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    ret = await hub.exec.gcp_api.client.compute.machine_image.list(
        ctx,
        project=project,
        filter=filter_,
        orderBy=order_by,
    )

    result["comment"] += ret["comment"]

    if not ret["result"]:
        result["result"] = False
        return result

    result["ret"] = ret["ret"].get("items", [])
    return result


async def get(
    hub, ctx, resource_id: str = None, project: str = None, name: str = None
) -> Dict[str, Any]:
    r"""Returns the specified machine image. Gets a list of available machine images by making a list() request.

    Args:
        name(str):
            The name of the machine image.

        project(str, Optional):
            Project ID for this request.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    if resource_id:
        ret = await hub.exec.gcp_api.client.compute.machine_image.get(
            ctx, resource_id=resource_id
        )
    else:
        ret = await hub.exec.gcp_api.client.compute.machine_image.get(
            ctx, project=project, machineImage=name
        )

    result["comment"] += ret["comment"]

    if not ret["result"]:
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result
