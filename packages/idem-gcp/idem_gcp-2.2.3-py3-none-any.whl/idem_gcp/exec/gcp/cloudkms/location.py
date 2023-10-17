"""Exec module for managing Cloud Key Management Service locations."""
from typing import Any
from typing import Dict


__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    resource_id: str,
):
    """Returns a location by its Idem resource ID.

    Args:
        resource_id(str):
            Idem resource ID. ``projects/{project id}/locations/{location id}``

    Returns:
        Location resource

    Examples:
        .. code-block:: sls

            {% set project_id = 'project-name' %}
            {% set location_id = 'us-east1' %}
            get-location:
                exec.run:
                    - path: gcp.cloudkms.location.get
                    - kwargs:
                          resource_id: projects/{{project_id}}/locations/{{location_id}}
    """
    result = {
        "comment": [],
        "ret": [],
        "result": True,
    }

    location = await hub.exec.gcp_api.client.cloudkms.projects.locations.get(
        ctx, _name=resource_id
    )

    if not location["result"]:
        result["comment"] += location["comment"]
        result["result"] = False
        return result

    result["ret"] = location["ret"]

    if not result["ret"]:
        result["comment"] += (
            hub.tool.gcp.comment_utils.get_empty_comment(
                "gcp.cloudkms.location", resource_id
            ),
        )

    return result


async def list_(
    hub, ctx, project: str = None, filter_: (str, "alias=filter") = None
) -> Dict[str, Any]:
    r"""Retrieves the locations for a specific project.

    Args:
        project(str, Optional):
            Project ID for this request. If not provided will use the one configured in `ctx`

        filter(str, Optional):
            A filter to narrow down results to a preferred subset. The filtering language accepts strings like
            "displayName=tokyo", and is documented in more detail in `AIP-160`_.

    .. _AIP-160: https://google.aip.dev/160

    Examples:
        .. code-block:: sls

            list-locations:
                exec.run:
                    - path: gcp.cloudkms.location.list
                    - kwargs:
                        project: project-name
    """
    result = {
        "comment": [],
        "ret": [],
        "result": True,
    }

    if project:
        name = f"projects/{project}"
    else:
        name = f"projects/{ctx.acct.project_id}"

    locations = await hub.exec.gcp_api.client.cloudkms.projects.locations.list(
        ctx, _name=name, filter=filter_
    )

    if not locations["result"]:
        result["comment"] += locations["comment"]
        result["result"] = False
        return result

    result["ret"] = locations["ret"].get("items", [])

    return result
