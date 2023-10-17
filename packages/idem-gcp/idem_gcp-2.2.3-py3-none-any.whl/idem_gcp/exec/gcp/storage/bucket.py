"""Exec module for managing Buckets."""
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def list_(
    hub,
    ctx,
    project: str = None,
    prefix: str = None,
    projection: str = "full",
):
    r"""Retrieves a list of buckets for a given project, ordered in the list lexicographically by name.

    Args:
        project(str, Optional):
            Project ID for this request.

        prefix(str, Optional):
            Filter results to buckets whose names begin with this prefix.

        projection(str, Optional):
            Set of properties to return. Defaults to noAcl.
            Acceptable values are:

           - full: Include all properties.
           - noAcl: Omit owner, acl, and defaultObjectAcl properties.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.storage.bucket.list
              - kwargs:
                  project: project-name
                  prefix: bucket-name-prefix
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    ret = await hub.exec.gcp_api.client.storage.bucket.list(
        ctx,
        project=project,
        prefix=prefix,
        projection=projection,
    )

    if not ret["result"]:
        result["comment"] += ret["comment"]
        result["result"] = False
        return result

    result["ret"] = ret["ret"].get("items", [])
    return result


async def get(
    hub,
    ctx,
    resource_id: str = None,
    name: str = None,
    projection: str = "full",
    user_project: str = None,
) -> Dict[str, Any]:
    r"""Returns the specified bucket.

    Args:
        resource_id(str, Optional):
            An identifier of the resource in the provider.

        name(str, Optional):
            Name of the bucket.

        projection(str, Optional):
            Set of properties to return. Defaults to noAcl.
            Acceptable values are:

            - full: Include all properties.
            - noAcl: Omit owner, acl, and defaultObjectAcl properties.

        user_project(str, Optional):
            The project to be billed for this request. Required for Requester Pays buckets.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.storage.bucket.get
              - kwargs:
                  name: bucket-name
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    ret = await hub.exec.gcp_api.client.storage.bucket.get(
        ctx,
        resource_id=resource_id,
        bucket=name,
        projection=projection,
        userProject=user_project,
    )

    if not ret["result"]:
        result["comment"] += ret["comment"]
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result


async def lock_retention_policy(
    hub,
    ctx,
    if_metageneration_match: str,
    name: str = None,
    user_project: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Locks retention policy on a bucket.

    Args:
        if_metageneration_match(str):
            Makes the operation conditional on whether bucket's current metageneration matches the given value.

        name(str, Optional):
            Name of the bucket.

        user_project(str, Optional):
            The project to be billed for this request. Required for Requester Pays buckets.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.storage.bucket.lock_retention_policy
              - kwargs:
                  name: bucket-name
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    ret = await hub.exec.gcp_api.client.storage.bucket.lockRetentionPolicy(
        ctx,
        resource_id=resource_id,
        bucket=name,
        if_metageneration_match=if_metageneration_match,
        user_project=user_project,
    )

    result["comment"] += ret["comment"]

    if not ret["result"]:
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result
