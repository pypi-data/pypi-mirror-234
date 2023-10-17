"""Exec module for managing Cloud Key Management Service key rings."""
from typing import Any
from typing import Dict


__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    resource_id: str,
):
    """Returns a key ring by its Idem resource ID.

    Args:
        resource_id(str):
            Idem resource ID. ``projects/{project id}/locations/{location id}/keyRings/{keyRing}``

    Returns:
        Key resource

    Examples:
        .. code-block:: sls

            {% set project_id = 'project-name' %}
            {% set location_id = 'us-east1' %}
            {% set key_ring = 'key-ring' %}
            get-key-ring:
                exec.run:
                    - path: gcp.cloudkms.key_ring.get
                    - kwargs:
                          resource_id: projects/{{project_id}}/locations/{{location_id}}/keyRings/{{key_ring}}
    """
    result = {
        "comment": [],
        "ret": [],
        "result": True,
    }

    key_ring = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.get(
        ctx, _name=resource_id
    )

    if not key_ring["result"]:
        result["comment"] += key_ring["comment"]
        result["result"] = False
        return result

    result["ret"] = key_ring["ret"]

    if not result["ret"]:
        result["comment"] += (
            hub.tool.gcp.comment_utils.get_empty_comment(
                "gcp.cloudkms.key_ring", resource_id
            ),
        )

    return result


async def list_(
    hub, ctx, location: str, filter_: (str, "alias=filter") = None, order_by: str = None
) -> Dict[str, Any]:
    r"""Retrieves key rings under specific location.

    Args:
        location(str):
            Location ID to be searched for key rings.

        filter(str, Optional):
            Only include resources that match the filter in the response. For more information, see
            `Sorting and filtering list results`_.

        order_by(str, Optional):
            Specify how the results should be sorted. If not specified, the results will be sorted in the default order.
            For more information, see `Sorting and filtering list results`_.

    .. _Sorting and filtering list results: https://cloud.google.com/kms/docs/sorting-and-filtering

    Examples:
        .. code-block:: sls

            list-locations:
                exec.run:
                   - path: gcp.cloudkms.location.list
                   - kwargs:
                         project: project-name

            #!require:list-locations
            list-key-rings:
                exec.run:
                   - path: gcp.cloudkms.key_ring.list
                   - kwargs:
                         location: {% for v in hub.idem.arg_bind.resolve('${exec:list-locations}') -%}
                                       {{ v['resource_id'] if v.get('display_name') == 'South Carolina' }}
                                   {%- endfor %}

            #!END

            list-global-key-rings:
                exec.run:
                   - path: gcp.cloudkms.key_ring.list
                   - kwargs:
                         location: projects/project-name/locations/global
                         filter_: NOT name=projects/project-name/locations/global/keyRings/kr-global-test
    """
    result = {
        "comment": [],
        "ret": [],
        "result": True,
    }

    key_rings = (
        await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.list(
            ctx, parent=location, filter=filter_, orderBy=order_by
        )
    )

    if not key_rings["result"]:
        result["comment"] += key_rings["comment"]
        result["result"] = False
        return result

    result["ret"] = key_rings["ret"].get("items", [])

    return result
