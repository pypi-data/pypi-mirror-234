"""Exec module for managing Snapshots."""
__func_alias__ = {"list_": "list"}

from typing import Dict, Any

from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext
from idem_gcp.tool.gcp.generate.exec_param import ExecParam


async def list_(
    hub,
    ctx,
    project: str = None,
    filter_: (str, "alias=filter") = None,
    order_by: str = None,
):
    r"""Retrieves the list of Snapshot resources contained within the specified project.

    Args:
        project(str, Optional):
            Project ID for this request.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = \"Intel Skylake\") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = \"Intel Skylake\") OR (cpuPlatform = \"Intel Broadwell\") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq \"double quoted literal\"` `(fieldname1 eq literal) (fieldname2 ne \"literal\")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name "instance", you would use `name ne .*instance`.

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy=\"creationTimestamp desc\"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.snapshot.list
              - kwargs:
                  project: project-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type="compute.snapshot",
        method_name="list",
        method_params={
            "ctx": ctx,
            "project": project,
            "filter": filter_,
            "order_by": order_by,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def get(
    hub,
    ctx,
    resource_id: str = None,
    project: str = None,
    name: str = None,
):
    r"""Returns the specified Snapshot resource. Gets a list of available snapshots by making a list() request.

    Args:
        resource_id(str, Optional):
            An identifier of the resource in the provider.

        project(str, Optional):
            Project ID for this request.

        name(str, Optional):
            Name of the snapshot resource to return.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.snapshot.get
              - kwargs:
                  project: project-name
                  name: snapshot-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type="compute.snapshot",
        method_name="get",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "snapshot": name,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def set_labels(
    hub,
    ctx,
    resource_id: str = None,
    project: str = None,
    resource: str = None,
    labels: Dict[str, Any] = None,
    label_fingerprint: str = None,
):
    r"""Sets the labels on a snapshot. To learn more about labels, read the Labeling Resources documentation.

    Args:
        resource_id(str, Optional):
            An identifier of the resource in the provider.

        project(str, Optional):
            Project ID for this request.

        resource(str, Optional):
            Name or id of the resource for this request.

        labels(Dict[str, Any], Optional):
            A list of labels to apply for this resource. Each label must comply with the requirements for labels. For example, \"webserver-frontend\": \"images\". A label value can also be empty (e.g. \"my-label\": \"\").

        label_fingerprint(str, Optional):
            The fingerprint of the previous set of labels for this resource, used to detect conflicts. The fingerprint is initially generated by Compute Engine and changes after every request to modify or update labels. You must always provide an up-to-date fingerprint hash when updating or changing labels, otherwise the request will fail with error 412 conditionNotMet. Make a get() request to the resource to get the latest fingerprint.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.snapshot.set_labels
              - kwargs:
                  project: project-name
                  resource: snapshot-name
                  labels:
                    label1: value1
                    label2: value2
                  label_fingerprint: IujiSXsfa3M=
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    request_body = {
        "labels": labels,
        "label_fingerprint": label_fingerprint,
    }

    execution_context = ExecutionContext(
        resource_type="compute.snapshot",
        method_name="setLabels",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "resource": resource,
            "body": request_body,
        },
        exec_params={
            ExecParam.PATH_PARAM_ALIASES: {
                # Path of snapshot#setLabels() has {resource}; others, e.g. snapshot#get(), have {snapshot} instead
                "snapshot": "resource",
            }
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)
