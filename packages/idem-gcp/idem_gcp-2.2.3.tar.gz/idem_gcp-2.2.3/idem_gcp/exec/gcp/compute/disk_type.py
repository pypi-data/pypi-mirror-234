"""Exec module for managing Disk Types."""
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def list_(
    hub,
    ctx,
    project: str = None,
    zone: str = None,
    region: str = None,
    filter_: (str, "alias=filter") = None,
    order_by: str = None,
    include_all_scopes: bool = False,
) -> Dict[str, Any]:
    r"""Retrieves a list of disk types available to the specified project.

    Args:
        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            The name of the zone for this request.

        region(str, Optional):
            The name of the region for this request.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = \"Intel Skylake\") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = \"Intel Skylake\") OR (cpuPlatform = \"Intel Broadwell\") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq \"double quoted literal\"` `(fieldname1 eq literal) (fieldname2 ne \"literal\")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name \"instance\", you would use `name ne .*instance`.

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy=\"creationTimestamp desc\"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported.

        include_all_scopes(bool, Optional):
            Indicates whether every visible scope for each scope type (zone, region, global) should be included in the response. For new resource types added after this field, the flag has no effect as new resource types will always include every visible scope for each scope type in response. For resource types which predate this field, if this flag is omitted or false, only scopes of the scope types where the resource type is expected to be found will be included.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.disk_type.list
              - kwargs:
                  project: project-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    result = dict(comment=[], ret=[], result=True)

    if zone and not include_all_scopes:
        ret = await hub.exec.gcp_api.client.compute.disk_type.list(
            ctx,
            project=project,
            zone=zone,
            filter=filter_,
            orderBy=order_by,
        )
    elif region and not include_all_scopes:
        ret = await hub.exec.gcp_api.client.compute.disk_type.list(
            ctx,
            project=project,
            region=region,
            filter=filter_,
            orderBy=order_by,
        )
    else:
        ret = await hub.exec.gcp_api.client.compute.disk_type.aggregatedList(
            ctx,
            project=project,
            filter=filter_,
            orderBy=order_by,
            includeAllScopes=include_all_scopes,
        )

    if not ret["result"]:
        result["comment"] += ret["comment"]
        result["result"] = False
        return result

    result["ret"] = ret["ret"].get("items", [])
    result["comment"] += ret["comment"]
    return result


async def get(
    hub,
    ctx,
    name: str = None,
    project: str = None,
    zone: str = None,
    region: str = None,
    resource_id: str = None,
):
    r"""Returns the specified disk type.

    Args:
        resource_id(str, Optional):
            An identifier of the resource in the provider.
            Defaults to None.

        name(str, Optional):
            Name of the machine type to return.

        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            The name of the zone for this request.

        region(str, Optional):
            The name of the region for this request.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.disk_type.get
              - kwargs:
                  name: disk-type-name
                  project: project-name
                  zone: zone-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    result = dict(comment=[], ret=[], result=True)

    if resource_id:
        ret = await hub.exec.gcp_api.client.compute.disk_type.get(
            ctx,
            resource_id=resource_id,
        )
    elif project and zone and name:
        ret = await hub.exec.gcp_api.client.compute.disk_type.get(
            ctx,
            project=project,
            zone=zone,
            diskType=name,
        )
    elif project and region and name:
        ret = await hub.exec.gcp_api.client.compute.disk_type.get(
            ctx,
            project=project,
            region=region,
            diskType=name,
        )
    else:
        result["result"] = False
        result["comment"] = [
            f"gcp.compute.disk_type {name} either resource_id or project, zone/region and name"
            f" should be specified."
        ]
        return result

    if not ret["result"]:
        result["comment"] += ret["comment"]
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    result["comment"] += ret["comment"]
    return result
