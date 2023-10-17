"""Exec module for managing Cloud Key Management Service import jobs."""
from typing import Any
from typing import Dict


__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    resource_id: str,
):
    """Returns a import job by its Idem resource ID.

    Args:
        resource_id(str):
            Idem resource ID. ``projects/{project id}/locations/{location id}/keyRings/{keyRing}/importJobs/{importJob}``

    Returns:
        ImportJob resource

    Examples:
        .. code-block:: sls

            {% set project_id = 'project-name' %}
            {% set location_id = 'us-east1' %}
            {% set key_ring = 'key-ring' %}
            {% set import_job = 'import-job' %}
            get-import-job:
                exec.run:
                    - path: gcp.cloudkms.import_job.get
                    - kwargs:
                        resource_id: projects/{{project_id}}/locations/{{location_id}}/keyRings/{{key_ring}}/importJobs/{{import_job}}
    """
    result = {
        "comment": [],
        "ret": [],
        "result": True,
    }

    import_job = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.import_jobs.get(
        ctx, _name=resource_id
    )

    if not import_job["result"]:
        result["comment"] += import_job["comment"]
        result["result"] = False
        return result

    result["ret"] = import_job["ret"]

    if not result["ret"]:
        result["comment"] += (
            hub.tool.gcp.comment_utils.get_empty_comment(
                "gcp.cloudkms.import_job", resource_id
            ),
        )

    return result


async def list_(
    hub, ctx, key_ring: str, filter_: (str, "alias=filter") = None, order_by: str = None
) -> Dict[str, Any]:
    r"""Retrieves import jobs in a key ring.

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
            list-import-jobs:
                exec.run:
                   - path: gcp.cloudkms.import_job.list
                   - kwargs:
                         key_ring: ${exec:list-key-rings:[0]:resource_id}

            #!END

            list-import-jobs-filtered:
                exec.run:
                   - path: gcp.cloudkms.import_job.list
                   - kwargs:
                         key_ring: projects/project-name/locations/global/keyRings/kr-global-test
                         filter_: expireTime < 2023-10-02
    """
    result = {
        "comment": [],
        "ret": [],
        "result": True,
    }

    import_jobs = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.import_jobs.list(
        ctx, parent=key_ring, filter=filter_, orderBy=order_by
    )
    if not import_jobs["result"]:
        result["comment"] += import_jobs["comment"]
        result["result"] = False
        return result

    result["ret"] = import_jobs["ret"].get("items", [])

    return result
