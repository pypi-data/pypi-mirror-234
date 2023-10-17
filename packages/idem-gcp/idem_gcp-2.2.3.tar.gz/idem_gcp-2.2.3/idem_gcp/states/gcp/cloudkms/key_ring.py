"""State module for managing Cloud Key Management Service key rings."""
from typing import Any
from typing import Dict

__contracts__ = ["resource"]
RESOURCE_TYPE = "cloudkms.key_ring"
RESOURCE_TYPE_FULL = "cloudkms.projects.locations.key_rings"
GCP_RESOURCE_TYPE_FULL = "gcp.cloudkms.key_ring"


async def present(
    hub,
    ctx,
    name: str,
    key_ring_id: str = None,
    project_id: str = None,
    location_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Create a new KeyRing in a given Project and Location.

    Args:
        name(str):
            Idem name.

        key_ring_id(str, Optional):
            Key ring id.

        project_id(str, Optional):
            Project id.

        location_id(str, Optional):
            Location id.

        resource_id(str, Optional):
            Idem resource id. Formatted as
            `projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}`

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            key_ring_present:
              gcp.cloudkms.key_ring.present:
                - key_ring_id: idem-gcp
                - project_id: tango-gcp
                - location_id: us-east1

    """
    result = {
        "result": True,
        "name": name,
        "old_state": None,
        "new_state": None,
        "comment": [],
    }

    if hub.tool.gcp.resource_prop_utils.properties_mismatch_resource_id(
        RESOURCE_TYPE_FULL,
        resource_id,
        {
            "project_id": project_id,
            "location_id": location_id,
            "key_ring_id": key_ring_id,
        },
    ):
        result["comment"].append(
            hub.tool.gcp.comment_utils.properties_mismatch_resource_id_comment(
                RESOURCE_TYPE_FULL, name
            )
        )

    get_resource_only_with_resource_id = hub.OPT.idem.get(
        "get_resource_only_with_resource_id", False
    )
    if resource_id:
        old_get_ret = await hub.exec.gcp.cloudkms.key_ring.get(
            ctx, resource_id=resource_id
        )

        if not old_get_ret["result"] or (
            not old_get_ret["ret"] and get_resource_only_with_resource_id
        ):
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        result["old_state"] = old_get_ret["ret"]
    elif not get_resource_only_with_resource_id:
        resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
            RESOURCE_TYPE_FULL,
            {
                "project_id": project_id,
                "location_id": location_id,
                "key_ring_id": key_ring_id,
            },
        )
        old_get_ret = await hub.exec.gcp.cloudkms.key_ring.get(
            ctx, resource_id=resource_id
        )

        if not old_get_ret["result"]:
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        if old_get_ret["ret"]:
            result["old_state"] = old_get_ret["ret"]

    if result["old_state"]:
        resource_id = result["old_state"].get("resource_id", None)

        els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
            RESOURCE_TYPE_FULL, resource_id
        )
        if (
            els.get("project_id") != project_id
            or els.get("location_id") != location_id
            or els.get("key_ring_id") != key_ring_id
        ):
            result["result"] = False
            result["comment"].append(
                hub.tool.gcp.comment_utils.non_updatable_properties_comment(
                    "gcp.cloudkms.key_ring",
                    key_ring_id,
                    ["project_id", "location_id", "key_ring_id"],
                )
            )
            return result
        result["comment"].append(
            hub.tool.gcp.comment_utils.already_exists_comment(
                "gcp.cloudkms.key_ring", key_ring_id
            )
        )
        result["old_state"] = old_get_ret["ret"]
        result["new_state"] = old_get_ret["ret"]
        result["new_state"]["name"] = name
        return result

    if ctx["test"]:
        plan_state = {"resource_id": resource_id, "name": name}
        result["comment"].append(
            hub.tool.gcp.comment_utils.would_create_comment(
                "gcp.cloudkms.key_ring", key_ring_id
            )
        )
        result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(plan_state)
        return result

    create_ret = (
        await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.create(
            ctx,
            parent=hub.tool.gcp.resource_prop_utils.construct_resource_id(
                "cloudkms.projects.locations",
                {"project_id": project_id, "location_id": location_id},
            ),
            key_ring_id=key_ring_id,
        )
    )
    if not create_ret["result"]:
        result["result"] = False
        result["comment"] += create_ret["comment"]
        return result
    result["comment"].append(
        hub.tool.gcp.comment_utils.create_comment("gcp.cloudkms.key_ring", key_ring_id)
    )
    result["old_state"] = {}
    resource_id = create_ret["ret"].get("resource_id")
    result["new_state"] = {"resource_id": resource_id, "name": name}
    return result


async def absent(
    hub,
    ctx,
    name: str,
) -> Dict[str, Any]:
    """Absent opreation is not supported for this resource.

    Args:
        name(str):
            Idem name.

    Returns:
        .. code-block:: json

            {
                "result": False,
                "comment": "...",
                "old_state": None,
                "new_state": None,
            }

    """
    return {
        "result": False,
        "name": name,
        "old_state": None,
        "new_state": None,
        "comment": [
            hub.tool.gcp.comment_utils.no_resource_delete_comment(
                "gcp.cloudkms.key_ring"
            )
        ],
    }


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieve the list of available key rings.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.cloudkms.key_ring
    """
    result = {}

    locations = await hub.exec.gcp.cloudkms.location.list(
        ctx, project=ctx.acct.project_id
    )
    if not locations["result"]:
        hub.log.debug(
            f"Could not describe gcp.cloudkms.key_ring in {ctx.acct.project_id} {locations['comment']}"
        )
        return {}

    for location in locations["ret"]:
        key_rings = await hub.exec.gcp.cloudkms.key_ring.list(
            ctx, location=location["resource_id"]
        )
        if not key_rings["result"]:
            hub.log.debug(
                f"Could not describe gcp.cloudkms.key_ring in {location['location_id']} {key_rings['comment']}"
            )
        else:
            for key_ring in key_rings["ret"]:
                resource_id = key_ring.get("resource_id")
                result[resource_id] = {
                    "gcp.cloudkms.key_ring.present": [
                        {parameter_key: parameter_value}
                        for parameter_key, parameter_value in key_ring.items()
                    ]
                }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
