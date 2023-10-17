"""Exec module for managing Instance Groups."""

__func_alias__ = {"list_": "list"}

from dataclasses import field
from dataclasses import make_dataclass
from typing import List

from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext
from idem_gcp.tool.gcp.generate.exec_param import ExecParam
from idem_gcp.tool.gcp.generate.scope import Scope


async def list_(
    hub,
    ctx,
    project: str = None,
    zone: str = None,
    filter_: (str, "alias=filter") = None,
    order_by: str = None,
):
    r"""Retrieves the list of zonal instance group resources contained within the specified zone. For managed instance groups, use the instanceGroupManagers or regionInstanceGroupManagers methods instead.

    Args:
        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            The name of the zone where the instance group is located.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = \"Intel Skylake\") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = \"Intel Skylake\") OR (cpuPlatform = \"Intel Broadwell\") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq \"double quoted literal\"` `(fieldname1 eq literal) (fieldname2 ne \"literal\")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name "instance", you would use `name ne .*instance`.

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy=\"creationTimestamp desc\"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance_group.list
              - kwargs:
                  project: project-name
                  zone: zone-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    # GCP method name is simply the name of this func or the one from __func_alias - we can pass it
    # also we can pass the resource name based on the file name
    execution_context = ExecutionContext(
        resource_type="compute.instance_group",
        method_name="list",
        method_params={
            "ctx": ctx,
            "project": project,
            "zone": zone,
            "filter": filter_,
            "order_by": order_by,
        },
        exec_params={
            ExecParam.SCOPED_FUNCTIONS: {
                Scope.ZONAL: "list",
                Scope.GLOBAL: "aggregatedList",
            }
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def get(
    hub,
    ctx,
    resource_id: str = None,
    project: str = None,
    zone: str = None,
    name: str = None,
):
    r"""Returns the specified zonal instance group. acceleratorTypes.get a list of available zonal instance groups by making a list() request. For managed instance groups, use the instanceGroupManagers or regionInstanceGroupManagers methods instead.

    Args:
        resource_id(str, Optional):
            An identifier of the resource in the provider.

        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            Name of the zone for this request.

        name(str, Optional):
            The name of the instance group. Authorization requires the following IAM permission on the specified resource instanceGroup: compute.instance_group.get.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance_group.get
              - kwargs:
                  project: project-name
                  zone: zone-name
                  name: instance-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type="compute.instance_group",
        method_name="get",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "zone": zone,
            "instanceGroup": name,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def list_instances(
    hub,
    ctx,
    instance_group_resource_id: str,
    filter_: (str, "alias=filter") = None,
    order_by: str = None,
):
    r"""Retrieves the list of instances in an instance groups.

    Args:
        instance_group_resource_id(str):
            Resource ID for the container instance group.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types
            of filter expressions: expressions that support regular expressions and expressions that follow API
            improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an
            operator, and the value that you want to use for filtering. The value must be a string, a number, or a
            boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are
            filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying
            `name != example-instance`. The `:` operator can be used with string fields to match substrings. For
            non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a
            key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You
            can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to
            include instances only if they are not scheduled for automatic restarts. You can use filtering on nested
            fields to filter based on resource labels. To filter on multiple expressions, provide each separate
            expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = \"Intel Skylake\") ```
            By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions
            explicitly. For example: ``` (cpuPlatform = \"Intel Skylake\") OR (cpuPlatform = \"Intel Broadwell\") AND (scheduling.automaticRestart = true) ```
            If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single
            un-parenthesized expression with or without quotes or against multiple parenthesized expressions.
            Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'`
            `fieldname eq \"double quoted literal\"` `(fieldname1 eq literal) (fieldname2 ne \"literal\")` The literal
            value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match
            the entire field. For example, to filter for instances that do not end with name "instance", you would use
            `name ne .*instance`.

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the
            resource name. You can also sort results in descending order based on the creation timestamp using
            `orderBy=\"creationTimestamp desc\"`. This sorts results based on the `creationTimestamp` field in reverse
            chronological order (newest result first). Use this to sort resources like operations so that the newest
            operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance_group.list_instances
              - kwargs:
                    instance_group_resource_id: projects/project-name/zones/us-central1-a/instanceGroups/instance-group
    """
    # GCP method name is simply the name of this func or the one from __func_alias - we can pass it
    # also we can pass the resource name based on the file name
    els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
        "compute.instance_group", instance_group_resource_id
    )
    execution_context = ExecutionContext(
        resource_type="compute.instance_group",
        method_name="listInstances",
        method_params={
            "ctx": ctx,
            "project": els["project"],
            "zone": els["zone"],
            "instance_group": els["instanceGroup"],
            "filter": filter_,
            "order_by": order_by,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def remove_instances(
    hub,
    ctx,
    instance_group_resource_id: str,
    instances: List[str],
):
    r"""Removes instances from an instance group.

    Args:
        instance_group_resource_id(str):
            Resource ID for the container instance group.

        instances(List[str]):
            Instance IDs of the instances to be removed.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance_group.remove_instances
              - kwargs:
                    instance_group_resource_id: projects/project-name/zones/us-central1-a/instanceGroups/instance-group
                    instances:
                        - projects/project-name/zones/us-central1-a/instances/instance-1
    """
    # GCP method name is simply the name of this func or the one from __func_alias - we can pass it
    # also we can pass the resource name based on the file name
    els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
        "compute.instance_group", instance_group_resource_id
    )
    execution_context = ExecutionContext(
        resource_type="compute.instance_group",
        method_name="removeInstances",
        method_params={
            "ctx": ctx,
            "project": els["project"],
            "zone": els["zone"],
            "instance_group": els["instanceGroup"],
            "body": {"instances": [{"instance": id} for id in instances]},
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def add_instances(
    hub,
    ctx,
    instance_group_resource_id: str,
    instances: List[str],
):
    r"""Adds instances to an instance group.

    Args:
        instance_group_resource_id(str):
            Resource ID for the container instance group.

        instances(List[str]):
            Instance IDs of the instances to be added.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance_group.add_instances
              - kwargs:
                    instance_group_resource_id: projects/project-name/zones/us-central1-a/instanceGroups/instance-group
                    instances:
                        - projects/project-name/zones/us-central1-a/instances/instance-1
    """
    # GCP method name is simply the name of this func or the one from __func_alias - we can pass it
    # also we can pass the resource name based on the file name
    els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
        "compute.instance_group", instance_group_resource_id
    )
    execution_context = ExecutionContext(
        resource_type="compute.instance_group",
        method_name="addInstances",
        method_params={
            "ctx": ctx,
            "project": els["project"],
            "zone": els["zone"],
            "instance_group": els["instanceGroup"],
            "body": {"instances": [{"instance": id} for id in instances]},
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def set_named_ports(
    hub,
    ctx,
    instance_group_resource_id: str,
    named_ports: List[
        make_dataclass(
            "NamedPort",
            [("name", str, field(default=None)), ("port", int, field(default=None))],
        )
    ] = None,
    fingerprint: str = None,
):
    r"""Sets the named ports for the specified instance group.

    Args:
        instance_group_resource_id(str):
            Resource ID for the container instance group.

        named_ports(List[Dict[str, Any]]):
            The list of named ports to set for this instance group.
            Assigns a name to a port number. For example: {name: "http", port: 80} This allows the system to reference ports by the assigned name instead of a port number. Named ports can also contain multiple ports. For example: [{name: "app1", port: 8080}, {name: "app1", port: 8081}, {name: "app2", port: 8082}] Named ports apply to all instances in this instance group. . Defaults to None.

            * name (str, Optional): The name for this named port. The name must be 1-63 characters long, and comply with RFC1035.
            * port (int, Optional): The port number, which can be a value between 1 and 65535.

        fingerprint(str):
            The fingerprint of the named ports information for this instance group. Use this optional property to prevent conflicts when multiple users change the named ports settings concurrently. Obtain the fingerprint with the instanceGroups.get method. Then, include the fingerprint in your request to ensure that you do not overwrite changes that were applied from another concurrent request. A request with an incorrect fingerprint will fail with error 412 conditionNotMet.
            A base64-encoded string.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance_group.set_named_ports
              - kwargs:
                    instance_group_resource_id: projects/project-name/zones/us-central1-a/instanceGroups/instance-group
                    fingerprint: ABCD
                    named_ports:
                        - name: http
                          port: 8080
    """
    # GCP method name is simply the name of this func or the one from __func_alias - we can pass it
    # also we can pass the resource name based on the file name
    els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
        "compute.instance_group", instance_group_resource_id
    )
    execution_context = ExecutionContext(
        resource_type="compute.instance_group",
        method_name="setNamedPorts",
        method_params={
            "ctx": ctx,
            "project": els["project"],
            "zone": els["zone"],
            "instance_group": els["instanceGroup"],
            "body": {
                "namedPorts": [np for np in named_ports],
                "fingerprint": fingerprint,
            },
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)
