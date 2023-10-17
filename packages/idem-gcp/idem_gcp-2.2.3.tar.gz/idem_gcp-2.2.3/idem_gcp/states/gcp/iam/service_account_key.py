"""State module for managing ServiceAccountKeys."""
from typing import Any
from typing import Dict

__contracts__ = ["resource"]
RESOURCE_TYPE = "iam.service_account_key"
RESOURCE_TYPE_FULL = f"gcp.{RESOURCE_TYPE}"


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    private_key_type: str = None,
    key_algorithm: str = None,
    key_origin: str = None,
    key_type: str = None,
    valid_before_time: str = None,
    valid_after_time: str = None,
    service_account_id: str = None,
):
    """Create a service account key.

    Args:
        name(str, Optional): The resource name of the service account key.
        resource_id(str, Optional): An identifier of the resource in the provider. Defaults to None.
        service_account_id(str, Optional): Required on create. The account resource id used to create a service key
        private_key_type(str, Optional): The output format of the private key. The default value is `TYPE_GOOGLE_CREDENTIALS_FILE`, which is the Google Credentials File format.
        key_algorithm(str, Optional): Which type of key and algorithm to use for the key. The default is currently a 2K RSA key. However this may change in the future.
        key_origin(str, Optional): The key origin. One of "ORIGIN_UNSPECIFIED", "USER_PROVIDED", "GOOGLE_PROVIDED".
        key_type(str, Optional): The key type. One of "KEY_TYPE_UNSPECIFIED", "USER_MANAGED", "SYSTEM_MANAGED"
        valid_before_time(str, Optional): The key can be used before this timestamp. For system-managed key pairs, this timestamp is the end time for the private key signing operation. The public key could still be used for verification for a few hours after this time.
        valid_after_time(str, Optional): The key can be used after this timestamp.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              gcp.iam.service_account_key.present:
              - private_key_type: TYPE_PKCS12_FILE
              - key_algorithm: KEY_ALG_RSA_2048
              - service_account_id: projects/project/serviceAccounts/test@test.iam.gserviceaccount.com
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    if resource_id:
        old_get_ret = await hub.exec.gcp.iam.service_account_key.get(
            ctx, resource_id=resource_id
        )

        if not old_get_ret["result"] or (not old_get_ret["ret"] and ctx["rerun_data"]):
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        result["old_state"] = old_get_ret["ret"]

    if result["old_state"]:
        resource_body = {
            "name": resource_id,
            "key_algorithm": key_algorithm,
            "key_origin": key_origin,
            "key_type": key_type,
            "valid_after_time": valid_after_time,
            "valid_before_time": valid_before_time,
        }
        resource_body = {k: v for (k, v) in resource_body.items() if v is not None}

        # no update operation is applicable to service account keys; simply compare states
        resource_body["resource_id"] = resource_id
        changes = hub.tool.gcp.utils.compare_states(
            result["old_state"],
            resource_body,
            RESOURCE_TYPE,
        )

        if not changes:
            result["comment"].append(
                hub.tool.gcp.comment_utils.up_to_date_comment(RESOURCE_TYPE_FULL, name)
            )
            result["new_state"] = result["old_state"]
            return result

        result["result"] = False
        result["comment"].append(
            hub.tool.gcp.comment_utils.no_resource_update_comment(
                RESOURCE_TYPE_FULL, resource_id
            )
        )
        return result
    else:
        resource_body = {
            "private_key_type": private_key_type,
            "key_algorithm": key_algorithm,
        }
        resource_body = {k: v for (k, v) in resource_body.items() if v is not None}

        if ctx.get("test", False):
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    RESOURCE_TYPE_FULL, name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                resource_body
            )
            result["new_state"]["resource_id"] = resource_id
            return result

        # Create
        create_ret = await hub.exec.gcp_api.client.iam.service_account_key.create(
            ctx,
            name=service_account_id,
            body=resource_body,
        )
        if not create_ret["result"] or not create_ret["ret"]:
            result["result"] = False
            if create_ret["comment"] and next(
                (
                    comment
                    for comment in create_ret["comment"]
                    if "alreadyExists" in comment
                ),
                None,
            ):
                result["comment"].append(
                    hub.tool.gcp.comment_utils.already_exists_comment(
                        RESOURCE_TYPE_FULL, name
                    )
                )
            else:
                result["comment"] += create_ret["comment"]
            return result

        result["comment"].append(
            hub.tool.gcp.comment_utils.create_comment(
                RESOURCE_TYPE_FULL, create_ret["ret"]["resource_id"]
            )
        )

        result["new_state"] = create_ret["ret"]

        return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
):
    r"""Deletes a service account key.

    Args:
        name(str):
            The name of the resource

        resource_id(str, Optional):
            The resource_id of the resource

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              gcp.iam.service_account_key.absent:
              - resource_id: resource-id
    """
    result = {
        "result": True,
        "old_state": ctx.get("old_state"),
        "new_state": None,
        "name": name,
        "comment": [],
    }

    if not resource_id:
        # we don't have enough information to know what to delete
        result["comment"].append(
            hub.tool.gcp.comment_utils.already_absent_comment(RESOURCE_TYPE_FULL, name)
        )
        return result

    get_ret = await hub.exec.gcp.iam.service_account_key.get(
        ctx, resource_id=resource_id
    )

    if not get_ret["result"]:
        result["result"] = False
        result["comment"].append(
            hub.tool.gcp.comment_utils.resource_not_found_comment(
                RESOURCE_TYPE_FULL, resource_id
            )
        )
        result["comment"].extend(get_ret["comment"])
        return result

    if not get_ret["ret"]:
        result["comment"].append(
            hub.tool.gcp.comment_utils.already_absent_comment(RESOURCE_TYPE_FULL, name)
        )
        return result

    result["old_state"] = get_ret["ret"]

    if ctx["test"]:
        result["comment"].append(
            hub.tool.gcp.comment_utils.would_delete_comment(RESOURCE_TYPE_FULL, name)
        )
        return result

    del_ret = await hub.exec.gcp_api.client.iam.service_account_key.delete(
        ctx, name=resource_id
    )

    if not del_ret["result"]:
        result["result"] = False
        result["comment"].extend(del_ret["comment"])
        return result

    result["comment"].append(
        hub.tool.gcp.comment_utils.delete_comment(RESOURCE_TYPE_FULL, name)
    )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves the list of available keys for a given service account.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.iam.service_account_key
    """
    result = {}

    list_accounts_ret = await hub.exec.gcp.iam.service_account.list(
        ctx, project=ctx.acct.project_id
    )

    if not list_accounts_ret["result"]:
        hub.log.debug(
            f"Could not describe {RESOURCE_TYPE_FULL} {list_accounts_ret['comment']}"
        )
        return result

    for resource in list_accounts_ret["ret"]:
        sa_resource_id = resource.get("resource_id")

        key_ret = await hub.exec.gcp.iam.service_account_key.list(
            ctx, project=ctx.acct.project_id, sa_resource_id=sa_resource_id
        )

        if not key_ret["result"]:
            hub.log.debug(
                f"Could not describe {RESOURCE_TYPE_FULL} in {sa_resource_id}: {key_ret['comment']}"
            )
        else:
            for service_account_key in key_ret["ret"]:
                resource_id = service_account_key.get("resource_id")
                result[resource_id] = {
                    "gcp.iam.service_account_key.present": [
                        {parameter_key: parameter_value}
                        for parameter_key, parameter_value in service_account_key.items()
                    ]
                }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
