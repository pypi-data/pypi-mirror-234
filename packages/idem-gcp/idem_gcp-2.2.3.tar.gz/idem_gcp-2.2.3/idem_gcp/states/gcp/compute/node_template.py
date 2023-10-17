"""State module for managing Node Templates."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from idem_gcp.tool.gcp.utils import regional_absent

# prevent commit hook from removing the import
absent = regional_absent

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    request_id: str = None,
    project: str = None,
    region: str = None,
    description: str = None,
    disks: List[
        make_dataclass(
            "LocalDisk",
            [
                ("disk_count", int, field(default=0)),
                ("disk_type", str, field(default=None)),
                ("disk_size_gb", int, field(default=0)),
            ],
        )
    ] = None,
    cpu_overcommit_type: str = None,
    server_binding: make_dataclass(
        "ServerBinding",
        [
            ("type_", (str, "alias=type"), field(default=None)),
        ],
    ) = None,
    node_affinity_labels: Dict = None,
    node_type_flexibility: make_dataclass(
        "NodeTemplateNodeTypeFlexibility",
        [
            ("memory", str, field(default=None)),
            ("local_ssd", str, field(default=None)),
            ("cpus", str, field(default=None)),
        ],
    ) = None,
    accelerators: List[
        make_dataclass(
            "AcceleratorConfig",
            [
                ("accelerator_type", str, field(default=None)),
                ("accelerator_count", int, field(default=0)),
            ],
        )
    ] = None,
    node_type: str = None,
) -> Dict[str, Any]:
    r"""Creates a network in the specified project using the data included in the request.

    Args:
        name(str):
            An Idem name of the resource.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        project(str, Optional):
            Project ID for this request.

        region(str, Optional):
            The name of the region for this request.

        description(str, Optional):
            An optional description of this resource. Provide this field when you create the resource. Defaults to None.

        disks(List[LocalDisk], Optional):
            Local disk configurations.

            * disk_count(int, Optional):
                Specifies the number of such disks.
            * disk_type(int, Optional):
                Specifies the size of the disk in base-2 GB.
            * disk_size_gb(str, Optional):
                Specifies the desired di…k type and not its URL.

        cpu_overcommit_type(str, Optional):
            CPU overcommit.

        server_binding(ServerBinding, Optional):
            Sets the binding properties for the physical server. Valid values include: - *[Default]* RESTART_NODE_ON_ANY_SERVER: Restarts VMs on any available physical server - RESTART_NODE_ON_MINIMAL_SERVER: Restarts VMs on the same physical server whenever possible See Sole-tenant node options for more information.

            * type(str, Optional):
                Enum type. Allowed values:
                    "RESTART_NODE_ON_ANY_SERVER"
                    "RESTART_NODE_ON_MINIMAL_SERVERS"
                    "SERVER_BINDING_TYPE_UNSPECIFIED"

        node_affinity_labels(Dict[str, Any], Optional):
            Labels to use for node affinity, which will be used in instance scheduling.

        node_type_flexibility(NodeTemplateNodeTypeFlexibility, Optional):
            Do not use. Instead, use the nodeType property.

            * memory(str, Optional):
                No description
            * local_ssd(str, Optional):
                No description
            * cpus(str, Optional):
                No description

        accelerators(List[AcceleratorConfig], Optional):
            A specification of the type and number of accelerator cards attached to the instance.

            * accelerator_type(int, Optional):
                The number of the guest …posed to this instance.
            * accelerator_count(str, Optional):
                Full or partial URL of t…t of accelerator types.

        node_type(str, Optional):
            The node type to use for nodes group that are created from this template.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

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
        "No-op: There is no create/update function for gcp.compute.node_template"
    )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves an aggregated list of node templates.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.node_template
    """
    result = {}

    # TODO: Pagination
    describe_ret = await hub.exec.gcp_api.client.compute.node_template.aggregatedList(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(
            f"Could not describe gcp.compute.node_template {describe_ret['comment']}"
        )
        return {}

    for resource in describe_ret["ret"].get("items", []):
        resource_id = resource.get("resource_id")

        result[resource_id] = {
            "gcp.compute.node_template.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
