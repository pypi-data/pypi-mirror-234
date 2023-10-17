"""Exec module for managing Cloud Key Management Service crypto keys."""
from typing import Any
from typing import Dict


__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    resource_id: str,
):
    """Returns a crypto key by its Idem resource ID.

    Args:
        resource_id(str):
            Idem resource ID. ``projects/{project id}/locations/{location id}/keyRings/{keyRing}/cryptoKeys/{cryptoKey}``

    Returns:
        CryptoKey resource

    Examples:
        .. code-block:: sls

            {% set project_id = 'project-name' %}
            {% set location_id = 'us-east1' %}
            {% set key_ring = 'key-ring' %}
            {% set crypto_key = 'crypto-key' %}
            get-crypto-key:
                exec.run:
                    - path: gcp.cloudkms.crypto_key.get
                    - kwargs:
                        resource_id: projects/{{project_id}}/locations/{{location_id}}/keyRings/{{key_ring}}/cryptoKeys/{{crypto_key}}
    """
    result = {
        "comment": [],
        "ret": [],
        "result": True,
    }

    crypto_key = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.get(
        ctx, _name=resource_id
    )

    if not crypto_key["result"]:
        result["comment"] += crypto_key["comment"]
        result["result"] = False
        return result

    result["ret"] = crypto_key["ret"]

    if not result["ret"]:
        result["comment"] += (
            hub.tool.gcp.comment_utils.get_empty_comment(
                "gcp.cloudkms.crypto_key", resource_id
            ),
        )

    return result


async def list_(
    hub, ctx, key_ring: str, filter_: (str, "alias=filter") = None, order_by: str = None
) -> Dict[str, Any]:
    r"""Retrieves the crypto keys in a key ring.

    Args:
        key_ring(str):
            key ring resource_id.

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

            #!require:list-key-rings
            list-crypto-keys:
                exec.run:
                   - path: gcp.cloudkms.crypto_key.list
                   - kwargs:
                         key_ring: ${exec:list-key-rings:[0]:resource_id}

            #!END

            list-crypto-keys-filtered:
                exec.run:
                   - path: gcp.cloudkms.crypto_key.list
                   - kwargs:
                         key_ring: projects/project-name/locations/global/keyRings/kr-global-test
                         filter: nextRotationTime < 2023-10-02
    """
    result = {
        "comment": [],
        "ret": [],
        "result": True,
    }

    crypto_keys = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.list(
        ctx, parent=key_ring, filter=filter_, orderBy=order_by
    )
    if not crypto_keys["result"]:
        result["comment"] += crypto_keys["comment"]
        result["result"] = False
        return result

    result["ret"] = crypto_keys["ret"].get("items", [])

    return result
