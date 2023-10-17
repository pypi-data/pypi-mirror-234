"""State module for managing Resource Policies."""
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
    project: str = None,
    region: str = None,
    resource_id: str = None,
    description: str = None,
    snapshot_schedule_policy: make_dataclass(
        "ResourcePolicySnapshotSchedulePolicy",
        [
            (
                "schedule",
                make_dataclass(
                    "ResourcePolicySnapshotSchedulePolicySchedule",
                    [
                        (
                            "daily_schedule",
                            make_dataclass(
                                "ResourcePolicyDailyCycle",
                                [
                                    ("days_in_cycle", int, field(default=0)),
                                    ("start_time", str, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        (
                            "weekly_schedule",
                            make_dataclass(
                                "ResourcePolicyWeeklyCycle",
                                [
                                    (
                                        "day_of_weeks",
                                        List[
                                            make_dataclass(
                                                "ResourcePolicyWeeklyCycleDayOfWeek",
                                                [
                                                    (
                                                        "start_time",
                                                        str,
                                                        field(default=None),
                                                    ),
                                                    ("day", str, field(default=None)),
                                                ],
                                            )
                                        ],
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                        (
                            "hourly_schedule",
                            make_dataclass(
                                "ResourcePolicyHourlyCycle",
                                [
                                    ("hours_in_cycle", int, field(default=0)),
                                    ("start_time", str, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
                field(default=None),
            ),
            (
                "retention_policy",
                make_dataclass(
                    "ResourcePolicySnapshotSchedulePolicyRetentionPolicy",
                    [
                        ("max_retention_days", int, field(default=0)),
                        ("on_source_disk_delete", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "snapshot_properties",
                make_dataclass(
                    "ResourcePolicySnapshotSchedulePolicySnapshotProperties",
                    [
                        ("guest_flush", bool, field(default=False)),
                        ("chain_name", str, field(default=None)),
                        ("storage_locations", List[str], field(default=None)),
                        ("labels", Dict[str, str], field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    group_placement_policy: make_dataclass(
        "ResourcePolicyGroupPlacementPolicy",
        [
            ("vm_count", int, field(default=0)),
            ("collocation", str, field(default=None)),
            ("availability_domain_count", int, field(default=0)),
        ],
    ) = None,
    instance_schedule_policy: make_dataclass(
        "ResourcePolicyInstanceSchedulePolicy",
        [
            ("start_time", str, field(default=None)),
            ("time_zone", str, field(default=None)),
            ("expiration_time", str, field(default=None)),
            (
                "vm_start_schedule",
                make_dataclass(
                    "ResourcePolicyInstanceSchedulePolicySchedule",
                    [
                        ("schedule", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "vm_stop_schedule",
                make_dataclass(
                    "ResourcePolicyInstanceSchedulePolicySchedule",
                    [
                        ("schedule", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    r"""Creates a new resource policy.

    You can use resource policies to schedule actions for some Compute Engine resources.
    For example, you can use them to schedule persistent disk snapshots.

    Args:
        name(str, Optional):
            An Idem name of the resource.

        project(str, Optional):
            Project ID for this request. Defaults to None.

        region(str, Optional):
            Name of the region for this request. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        description(str, Optional):
            An optional description of this resource. Defaults to None.

        snapshot_schedule_policy(Dict[str, Any], Optional):
            Resource policy for persistent disks for creating snapshots. Defaults to None.
            A snapshot schedule policy specifies when and how frequently snapshots are to be created for
            the target disk. Also specifies how many and how long these scheduled snapshots should be retained.

            * schedule(Dict[str, Any], Optional):
                A Vm Maintenance Policy specifies what kind of infrastructure maintenance we are allowed to perform on
                this VM and when. Schedule that is applied to disks covered by this policy.
                A schedule for disks where the scheduled operations are performed.

                * daily_schedule(Dict[str, Any], Optional):
                    Time window specified for daily operations.

                    * days_in_cycle(int, Optional):
                        Defines a schedule with units measured in days.
                        The value determines how many days pass between the start of each cycle.

                    * start_time(str, Optional):
                        Start time of the window. This must be in UTC format that resolves to one of
                        00:00, 04:00, 08:00, 12:00, 16:00, or 20:00. For example, both 13:00-5 and 08:00 are valid.

                * weekly_schedule(Dict[str, Any], Optional):
                    Time window specified for weekly operations.

                    * day_of_weeks(List[Dict[str, Any]], Optional):
                        Up to 7 intervals/windows, one for each day of the week.

                        * start_time(str, Optional):
                            Time within the window to start the operations.
                            It must be in format \"HH:MM\", where HH : [00-23] and MM : [00-00] GMT.

                        * day(str, Optional):
                            Defines a schedule that runs on specific days of the week. Specify one or more days.
                            The following options are available:
                            MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY.

                * hourly_schedule(Dict[str, Any], Optional):
                    Time window specified for hourly operations.

                    * hours_in_cycle(int, Optional):
                        Defines a schedule with units measured in hours.
                        The value determines how many hours pass between the start of each cycle.

                    * start_time(str, Optional):
                        Time within the window to start the operations.
                        It must be in format \"HH:MM\", where HH : [00-23] and MM : [00-00] GMT.

            * retention_policy(Dict[str, Any], Optional):
                Retention policy applied to snapshots created by this resource policy.
                Policy for retention of scheduled snapshots.

                * max_retention_days(int, Optional):
                    Maximum age of the snapshot that is allowed to be kept.

                * on_source_disk_delete(str, Optional):
                    Specifies the behavior to apply to scheduled snapshots when the source disk is deleted.
                    The following options are available:
                    APPLY_RETENTION_POLICY, KEEP_AUTO_SNAPSHOTS, UNSPECIFIED_ON_SOURCE_DISK_DELETE


            * snapshot_properties(Dict[str, Any], Optional):
                Properties with which snapshots are created such as labels, encryption keys.
                Specified snapshot properties for scheduled snapshots created by this policy.

                * guest_flush(bool, Optional):
                    Indication to perform a 'guest aware' snapshot.

                * chain_name(str, Optional):
                    Chain name that the snapshot is created in.

                * storage_locations(List[str, str], Optional):
                    Cloud Storage bucket storage location of the auto snapshot (regional or multi-regional).

                * labels(List[str, str], Optional):
                    Labels to apply to scheduled snapshots. These can be later modified by the setLabels method.
                    Label values may be empty.

        group_placement_policy(Dict[str, Any], Optional):
            Resource policy for instances for placement configuration. Defaults to None.
            A GroupPlacementPolicy specifies resource placement configuration.
            It specifies the failure bucket separation as well as network locality

            * vm_count(int, Optional):
                Number of VMs in this placement group. Google does not recommend that you use this field unless
                you use a compact policy, and you want your policy to work only if it contains this exact number of VMs.

            * collocation(str, Optional):
                Specifies network collocation. The following options are available:
                COLLOCATED, UNSPECIFIED_COLLOCATION

            * availability_domain_count(int, Optional):
                The number of availability domains to spread instances across.
                If two instances are in different availability domain, they are not in the same low latency network.

        instance_schedule_policy(Dict[str, Any], Optional):
            Resource policy for scheduling instance operations. Defaults to None.
            An InstanceSchedulePolicy specifies when and how frequent certain operations are performed on the instance.

            * start_time(str, Optional):
                The start time of the schedule. The timestamp is an RFC3339 string.

            * time_zone(str, Optional):
                Specifies the time zone to be used in interpreting Schedule.schedule.
                The value of this field must be a time zone name from the tz database:
                http://en.wikipedia.org/wiki/Tz_database.

            * expiration_time(str, Optional):
                The expiration time of the schedule. The timestamp is an RFC3339 string.

            * vm_start_schedule(Dict[str, Any], Optional):
                Specifies the schedule for starting instances.

                * schedule(str, Optional):
                    Specifies the frequency for the operation, using the unix-cron format.

            * vm_stop_schedule(Dict[str, Any], Optional):
                Specifies the schedule for stopping instances.

                * schedule(str, Optional):
                    Specifies the frequency for the operation, using the unix-cron format.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            example_resource_name:
              gcp.compute.resource_policy.present:
                - name: value
                - project: value
                - region: value
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
        "No-op: There is no create/update function for gcp.compute.resource_policy"
    )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves a list of resource policies contained within the specified region.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.resource_policy
    """
    result = {}

    describe_ret = await hub.exec.gcp.compute.resource_policy.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(f"Could not describe resource policies {describe_ret['comment']}")
        return {}

    for resource in describe_ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "gcp.compute.resource_policy.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
