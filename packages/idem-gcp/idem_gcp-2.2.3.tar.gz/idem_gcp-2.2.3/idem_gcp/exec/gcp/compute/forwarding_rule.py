"""Exec module for managing ForwardingRule."""
from typing import Any
from typing import Dict

from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext
from idem_gcp.tool.gcp.generate.exec_param import ExecParam
from idem_gcp.tool.gcp.generate.scope import Scope

__func_alias__ = {"list_": "list"}


async def list_(
    hub,
    ctx,
    project: str = None,
    region: str = None,
    filter_: (str, "alias=filter") = None,
    order_by: str = None,
):
    r"""Retrieves the list of ForwardingRule resources available to the specified project.

    Args:
        project(str, Optional):
            Project ID for this request.

        region(str, Optional):
            The name of the region for this request.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = \"Intel Skylake\") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = \"Intel Skylake\") OR (cpuPlatform = \"Intel Broadwell\") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq \"double quoted literal\"` `(fieldname1 eq literal) (fieldname2 ne \"literal\")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name "instance", you would use `name ne .*instance`.

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy=\"creationTimestamp desc\"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.forwarding_rule.list
              - kwargs:
                  project: project-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type="compute.forwarding_rule",
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
    region: str = None,
    name: str = None,
    project: str = None,
    resource_id: str = None,
):
    r"""Returns the specified ForwardingRule resource. Gets a list of available forwarding rules by making a list() request.

    Args:
        project(str, Optional):
            Project ID for this request. Defaults to None.

        region(str, Optional):
            The name of the region for this request.

        name(str, Optional):
            Name of the resource to return. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.forwarding_rule.get
              - kwargs:
                  project: project-name
                  name: forwarding-rule-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type="compute.forwarding_rule",
        method_name="get",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "region": region,
            "forwardingRule": name,
        },
    )

    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def set_target(
    hub,
    ctx,
    target: str,
    forwarding_rule: str = None,
    project: str = None,
    region: str = None,
    resource_id: str = None,
):
    r"""Changes target URL for the GlobalForwardingRule resource. The new target should be of the same type as the old target.

    Args:
        target(str):
            The URL of the target resource to receive the matched traffic. For regional forwarding rules, this target must be in the same region as the forwarding rule. For global forwarding rules, this target must be a global load balancing resource. The forwarded traffic must be of a type appropriate to the target object. - For load balancers, see the \"Target\" column in [Port specifications](https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications). - For Private Service Connect forwarding rules that forward traffic to Google APIs, provide the name of a supported Google API bundle: - vpc-sc - APIs that support VPC Service Controls. - all-apis - All supported Google APIs. - For Private Service Connect forwarding rules that forward traffic to managed services, the target must be a service attachment.

        forwarding_rule(str, Optional):
            Name of the ForwardingRule resource in which target is to be set.

        project(str, Optional):
            Project ID for this request. Defaults to None.

        region(str, Optional):
            The name of the region for this request.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.forwarding_rule.get
              - kwargs:
                  project: project-name
                  name: forwarding-rule-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type="compute.forwarding_rule",
        method_name="setTarget",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "region": region,
            "forwarding_rule": forwarding_rule,
            "body": {"target": target},
        },
    )

    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def set_labels(
    hub,
    ctx,
    labels: Dict[str, Any],
    label_fingerprint: str,
    resource_id: str = None,
    project: str = None,
    region: str = None,
    resource: str = None,
):
    r"""Sets the labels on a forwarding rule. To learn more about labels, read the Labeling Resources documentation.

    Args:
        labels(Dict[str, Any]):
            A list of labels to apply for this resource. Each label must comply with the requirements for labels. For example, \"webserver-frontend\": \"images\". A label value can also be empty (e.g. \"my-label\": \"\").

        label_fingerprint(str):
            The fingerprint of the previous set of labels for this resource, used to detect conflicts. The fingerprint is initially generated by Compute Engine and changes after every request to modify or update labels. You must always provide an up-to-date fingerprint hash when updating or changing labels, otherwise the request will fail with error 412 conditionNotMet. Make a get() request to the resource to get the latest fingerprint.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

        project(str, Optional):
            Project ID for this request.

        region(str, Optional):
            The name of the region for this request.

        resource(str, Optional):
            Name or id of the resource for this request.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.forwarding_rule.set_labels
              - kwargs:
                  project: project-name
                  resource: forwarding-rule-name
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
        resource_type="compute.forwarding_rule",
        method_name="setLabels",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "region": region,
            "resource": resource,
            "body": request_body,
        },
        exec_params={
            ExecParam.PATH_PARAM_ALIASES: {
                # Path of forwardingRule#setLabels() has {resource}; others, e.g. forwardingRule#get(), have {forwardingRule} instead
                "forwardingRule": "resource",
            }
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)
