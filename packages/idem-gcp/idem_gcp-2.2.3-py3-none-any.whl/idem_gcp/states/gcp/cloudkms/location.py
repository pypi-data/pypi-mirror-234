"""State module for managing Cloud Key Management Service locations."""
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
) -> Dict[str, Any]:
    """Present operation is not supported for this resource.

    Args:
        name(str):
            Idem name.

    Returns:
        .. code-block:: json

            {
                "result": False,
                "comment": "...",
            }

    """
    return {
        "result": False,
        "name": name,
        "old_state": None,
        "new_state": None,
        "comment": [
            hub.tool.gcp.comment_utils.no_resource_create_update_comment(
                "gcp.cloudkms.location"
            )
        ],
    }


async def absent(
    hub,
    ctx,
    name: str,
) -> Dict[str, Any]:
    """Absent operation is not supported for this resource.

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
            hub.tool.gcp.comment_utils.no_resource_create_update_comment(
                "gcp.cloudkms.location"
            )
        ],
    }


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Retrieve the list of available locations.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.cloudkms.location
    """
    result = {}

    locations = await hub.exec.gcp.cloudkms.location.list(
        ctx, project=ctx.acct.project_id
    )
    if not locations["result"]:
        hub.log.debug(
            f"Could not describe gcp.cloudkms.location in {ctx.acct.project_id} {locations['comment']}"
        )
        return {}

    for location in locations["ret"]:
        resource_id = location.get("resource_id")
        result[resource_id] = {
            "gcp.cloudkms.location.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in location.items()
            ]
        }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
