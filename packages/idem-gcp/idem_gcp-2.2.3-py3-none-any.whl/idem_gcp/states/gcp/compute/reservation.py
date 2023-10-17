"""State module for managing Reservations."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from idem_gcp.tool.gcp.utils import zonal_absent

# prevent commit hook from removing the import
absent = zonal_absent

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    request_id: str = None,
    project: str = None,
    zone: str = None,
    description: str = None,
    share_settings: make_dataclass(
        "ShareSettings",
        [
            (
                "project_map",
                make_dataclass(
                    "ShareSettingsProjectConfig",
                    [("project_id", str, field(default=None))],
                ),
                field(default=None),
            ),
            ("share_type", str, field(default="LOCAL")),
        ],
    ) = None,
    specific_reservation: make_dataclass(
        "AllocationSpecificSKUReservation",
        [
            ("count", str, field(default=None)),
            (
                "instance_properties",
                make_dataclass(
                    "AllocationSpecificSKUAllocationReservedInstanceProperties",
                    [
                        ("machine_type", str, field(default=None)),
                        (
                            "local_ssds",
                            List[
                                make_dataclass(
                                    "AllocationSpecificSKUAllocationAllocatedInstancePropertiesReservedDisk",
                                    [
                                        ("disk_size_gb", str, field(default=None)),
                                        ("interface", str, field(default=None)),
                                    ],
                                )
                            ],
                            field(default=None),
                        ),
                        ("location_hint", str, field(default=None)),
                        ("guest_accelerators", str, field(default=None)),
                        ("min_cpu_platform", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    specific_reservation_required: bool = False,
) -> Dict[str, Any]:
    r"""Creates a new reservation. For more information, read Reserving zonal resources.

    Args:
        name(str):
            An Idem name of the resource.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            Name of the zone for this request.

        description(str, Optional):
            An optional description of this resource. Provide this field when you create the resource. Defaults to None.

        share_settings(Dict[str, Any], Optional):
            Share-settings for shared-reservation

            * project_map(Dict[str, Any], Optional):
                A map of project id and project config. This is only valid when share_type's value is SPECIFIC_PROJECTS.
                * project_id(str, Optional):
                    The project ID, should be same as the key of this project config in the parent map.
            * share_type(str, Optional):
                Type of sharing for this shared-reservation
                Enum type. Allowed values:
                    "LOCAL"
                    "ORGANIZATION"
                    "SHARE_TYPE_UNSPECIFIED"
                    "SPECIFIC_PROJECTS"

        specific_reservation(Dict[str, Any], Optional):
            Reservation for instances with specific machine shapes.

            * count(str, Optional):
                Specifies the number of resources that are allocated.
            * instance_properties(Dict[str, Any], optional):
                The instance properties for the reservation.
                * machine_type(str, Optional):
                    Specifies type of machine (name only) which has fixed number of vCPUs and fixed amount
                    of memory. This also includes specifying custom machine type following custom-NUMBER_OF_CPUS-AMOUNT_OF_MEMORY pattern.
                * local_ssds(List[Dict[str, Any]], Optional):
                    Specifies amount of local ssd to reserve with each instance. The type of disk is local-ssd.
                    * disk_size_gb(int, Optional):
                        Specifies the size of the disk in base-2 GB.
                    * interface(str, Optional):
                        Specifies the disk interface to use for attaching this disk, which is either SCSI or NVME. The default is SCSI.
                        For performance characteristics of SCSI over NVMe, see Local SSD performance.
                        Enum type. Allowed values:
                            "NVME"
                            "SCSI"
                * location_hint(str, Optional):
                    An opaque location hint used to place the allocation close to other resources. This field is for use by internal tools that use the public API.
                * guest_accelerators(List[AcceleratorConfig], Optional):
                    Specifies accelerator type and count.
                * min_cpu_platform(str, Optional):
                    Minimum cpu platform the reservation.

        specific_reservation_required(bool, Optional):
            Indicates whether the reservation can be consumed by VMs with affinity for \"any\" reservation. If the field is set, then only VMs that target the reservation by name can consume from this reservation.

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
        "No-op: There is no create/update function for gcp.compute.reservation"
    )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves a list of all the reservations that have been configured for the specified project in specified zone.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.reservation
    """
    result = {}

    # TODO: Pagination
    describe_ret = await hub.exec.gcp_api.client.compute.reservation.aggregatedList(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(
            f"Could not describe gcp.compute.reservation {describe_ret['comment']}"
        )
        return {}

    for resource in describe_ret["ret"].get("items", []):
        resource_id = resource.get("resource_id")

        result[resource_id] = {
            "gcp.compute.reservation.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
