"""Exec module for managing Node Templates."""
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def list_(
    hub,
    ctx,
    project: str = None,
    region: str = None,
    filter_: (str, "alias=filter") = None,
    max_results: int = 500,
    order_by: str = None,
    page_token: str = None,
    return_partial_success: bool = False,
) -> Dict[str, Any]:
    r"""Retrieves a list of node templates available to the specified project.

    Args:
        project(str, Optional):
            Project ID for this request.

        region(str, Optional):
            The name of the region for this request.

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
              - path: gcp.compute.node_template.list
              - kwargs:
                  project: project-name
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    if region:
        ret = await hub.exec.gcp_api.client.compute.node_template.list(
            ctx,
            project=project,
            region=region,
            filter=filter_,
            maxResults=max_results,
            orderBy=order_by,
            pageToken=page_token,
            returnPartialSuccess=return_partial_success,
        )
    else:
        ret = await hub.exec.gcp_api.client.compute.node_template.aggregatedList(
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
    hub,
    ctx,
    resource_id: str = None,
    region: str = None,
    name: str = None,
    project: str = None,
) -> Dict[str, Any]:
    r"""Returns the specified node template. Gets a list of available node templates by making a list() request.

    Args:

        resource_id(str, Optional):
            An identifier of the resource in the provider.

        region(str, Optional):
            The name of the region for this request.

        name(str, Optional):
            Name of the node template to return.

        project(str, Optional):
            Project ID for this request.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.node_template.get
              - kwargs:
                  project: project-name
                  region: region
                  name: node-template-name
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    if resource_id:
        ret = await hub.exec.gcp_api.client.compute.node_template.get(
            ctx,
            resource_id=resource_id,
        )
    elif project and region and name:
        ret = await hub.exec.gcp_api.client.compute.node_template.get(
            ctx, project=project, region=region, nodeTemplate=name
        )
    else:
        result["result"] = False
        result["comment"] = [
            f"gcp.compute.node_template#get(): {name} either resource_id or project, region and name should be specified."
        ]
        return result

    if not ret["result"]:
        result["comment"] += ret["comment"]
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result
