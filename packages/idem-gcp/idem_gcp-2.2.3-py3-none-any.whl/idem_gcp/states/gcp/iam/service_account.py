"""State module for managing Service Accounts."""
import copy
from typing import Any
from typing import Dict


__contracts__ = ["resource"]
RESOURCE_TYPE = "iam.service_account"
RESOURCE_TYPE_FULL = f"gcp.{RESOURCE_TYPE}"


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    project_id: str = None,
    account_id: str = None,
    display_name: str = None,
    description: str = None,
    unique_id: str = None,
    email: str = None,
    etag: str = None,
    disabled: bool = None,
    oauth2_client_id: str = None,
) -> Dict[str, Any]:
    """Create or update a service account resource.

    Args:
        name(str, Optional):
            The resource name of the service account.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        project_id(str, Optional):
            A valid API project identifier.

        account_id(str):
            Required on create. The account id that is used to generate the service account email address
            and a stable unique id. It is unique within a project, must be 6-30 characters long, and match the regular
            expression [a-z]([-a-z0-9]*[a-z0-9]) to comply with RFC1035.

        display_name(str, Optional):
            A user-specified, human-readable name for the service account. The maximum length is 100 UTF-8 bytes.

        description(str, Optional):
            A user-specified, human-readable description of the service account. The maximum length is 256 UTF-8 bytes.

        unique_id(str, Optional):
            The unique, stable numeric ID for the service account.

        email(str, Optional):
            The email address of the service account.

        etag(str, Optional):
            A base64-encoded string.

        disabled(str, Optional):
            Output only. Whether the service account is disabled.

        oauth2_client_id(str, Optional):
            The OAuth 2.0 client ID for the service account.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              gcp.iam.service_account.present:
                - name: value
                - project_id: value
    """
    project_id = hub.tool.gcp.utils.get_project_from_account(ctx, project_id)

    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    # Wait until resource is available in GCP
    if ctx.get("rerun_data"):
        service_account = ctx.get("rerun_data").get("old_state")

        old_get_ret = await hub.exec.gcp.iam.service_account.get(
            ctx, resource_id=service_account["resource_id"]
        )

        if not old_get_ret["result"]:
            result["comment"] += old_get_ret["comment"]
            result["rerun_data"] = ctx.get("rerun_data")
            return result

        result["old_state"] = service_account
        result["new_state"] = old_get_ret["ret"]

        return result

    get_resource_only_with_resource_id = hub.OPT.idem.get(
        "get_resource_only_with_resource_id", False
    )

    if resource_id:
        old_get_ret = await hub.exec.gcp.iam.service_account.get(
            ctx, resource_id=resource_id
        )

        if not old_get_ret["result"] or (
            not old_get_ret["ret"] and get_resource_only_with_resource_id
        ):
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        result["old_state"] = hub.tool.gcp.utils.convert_to_regular_dict(
            old_get_ret["ret"]
        )
    elif not get_resource_only_with_resource_id:
        resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
            RESOURCE_TYPE, locals()
        )

        get_ret = await hub.exec.gcp.iam.service_account.get(
            ctx, resource_id=resource_id, name=name
        )

        if not get_ret["result"]:
            result["result"] = False
            result["comment"] += get_ret["comment"]
            return result

        if get_ret["ret"]:
            result["old_state"] = get_ret["ret"]

    if result["old_state"]:
        new_state = {
            "name": name,
            "resource_id": resource_id,
            "project_id": project_id,
            "unique_id": unique_id,
            "email": email,
            "display_name": display_name,
            "etag": etag,
            "oauth2_client_id": oauth2_client_id,
            "description": description,
            "disabled": disabled,
        }
        new_state = {k: v for (k, v) in new_state.items() if v is not None}

        changes = hub.tool.gcp.utils.compare_states(
            result["old_state"],
            new_state,
            RESOURCE_TYPE,
            additional_exclude_paths=["name"],
        )
        if not changes:
            result["comment"].append(
                hub.tool.gcp.comment_utils.up_to_date_comment(RESOURCE_TYPE_FULL, name)
            )
            result["new_state"] = result["old_state"]
            return result

        changed_non_updatable_properties = (
            hub.tool.gcp.resource_prop_utils.get_changed_non_updatable_properties(
                RESOURCE_TYPE, changes
            )
        )
        if changed_non_updatable_properties:
            result["result"] = False
            result["comment"].append(
                hub.tool.gcp.comment_utils.non_updatable_properties_comment(
                    RESOURCE_TYPE_FULL,
                    name,
                    changed_non_updatable_properties,
                )
            )
            result["new_state"] = result["old_state"]
            return result

        update_mask = []
        service_account = {}
        if display_name is not None and display_name != result["old_state"].get(
            "display_name"
        ):
            service_account["display_name"] = display_name
            update_mask.append("displayName")
        if description is not None and description != result["old_state"].get(
            "description"
        ):
            service_account["description"] = description
            update_mask.append("description")

        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_update_comment(
                    RESOURCE_TYPE_FULL, result["old_state"]["resource_id"]
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                {**result["old_state"], **service_account}
            )
            return result

        patch_ret = await hub.exec.gcp_api.client.iam.service_account.patch(
            ctx,
            name=resource_id,
            body={
                "service_account": service_account,
                "update_mask": ",".join(update_mask),
            },
        )
        if not patch_ret["result"]:
            result["result"] = False
            result["comment"] += patch_ret["comment"]
            return result

        result["new_state"] = {
            **result["old_state"],
            **patch_ret["ret"],
            **service_account,
        }
        result["comment"].append(
            hub.tool.gcp.comment_utils.update_comment(
                RESOURCE_TYPE_FULL, result["new_state"]["resource_id"]
            )
        )
        return result
    else:
        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    RESOURCE_TYPE_FULL, resource_id
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                {
                    "resource_id": resource_id,
                    "name": name,
                    "project_id": project_id,
                    "unique_id": unique_id,
                    "email": email,
                    "display_name": display_name,
                    "etag": etag,
                    "oauth2_client_id": oauth2_client_id,
                }
            )
            return result

        # Create
        if not account_id:
            result["result"] = False
            result["comment"].append("Property 'account_id' is required.")
            return result

        resource_body = {"account_id": account_id}
        service_account = {"display_name": display_name, "description": description}
        service_account = {k: v for (k, v) in service_account.items() if v is not None}
        if service_account:
            resource_body["service_account"] = service_account

        create_ret = await hub.exec.gcp_api.client.iam.service_account.create(
            ctx, name=f"projects/{project_id}", body=resource_body
        )

        if not create_ret["result"]:
            result["result"] = False
            result["comment"] += create_ret["comment"]
            return result

        result["comment"].append(
            hub.tool.gcp.comment_utils.create_comment(
                RESOURCE_TYPE_FULL, create_ret["ret"]["resource_id"]
            )
        )

        result["rerun_data"] = {
            "operation": "create",
            "old_state": {
                **copy.copy(create_ret["ret"]),
            },
        }

        return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    r"""Deletes a service account.

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
              gcp.iam.service_account.absent:
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

    get_ret = await hub.exec.gcp.iam.service_account.get(ctx, resource_id=resource_id)

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

    del_ret = await hub.exec.gcp_api.client.iam.service_account.delete(
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

    Lists every ServiceAccount that belongs to a specific project.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.iam.service_accounts
    """
    result = {}

    describe_ret = await hub.exec.gcp.iam.service_account.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(
            f"Could not describe gcp.iam.service_account {describe_ret['comment']}"
        )
        return {}

    for resource in describe_ret["ret"]:
        resource_id = resource.get("resource_id")

        result[resource_id] = {
            "gcp.iam.service_account.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
