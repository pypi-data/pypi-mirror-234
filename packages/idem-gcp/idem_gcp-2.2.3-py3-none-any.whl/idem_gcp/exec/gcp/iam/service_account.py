"""Exec module for managing ServiceAccounts."""
import re
from typing import Callable

from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext

__func_alias__ = {"list_": "list"}
RESOURCE_TYPE = "iam.service_account"
RESOURCE_TYPE_FULL = f"gcp.{RESOURCE_TYPE}"


async def list_(hub, ctx, project: str = None):
    r"""Lists every ServiceAccount that belongs to a specific project.

    Args:
        project(str, Required):
            The resource name of the project associated with the service accounts.
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type=RESOURCE_TYPE,
        method_name="list",
        method_params={"ctx": ctx, "name": f"projects/{project}"},
    )

    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def get(
    hub,
    ctx,
    project_id: str = None,
    unique_id: str = None,
    email: str = None,
    name: str = None,
    resource_id: str = None,
):
    r"""Returns the specified ServiceAccount resource.

    Args:
        project_id(str, Optional):
            Project ID for this request.
        unique_id(str, Optional):
            The unique, stable numeric ID for the service account.
        email(str, Optional):
            The email address of the service account.
        name(str, Optional):
            Name of the service account in the provider API.
        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.iam.service_account.get
              - kwargs:
                  name: service-account-name
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }
    if not resource_id:
        project_id = hub.tool.gcp.utils.get_project_from_account(ctx, project_id)
        resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
            RESOURCE_TYPE, locals()
        )

    if not resource_id and re.match(r"^projects/.+/serviceAccounts/.+$", name or ""):
        resource_id = name

    if not resource_id:
        result["comment"] = [
            f"{RESOURCE_TYPE_FULL}#get(): either resource_id or name or unique_id or email"
            f" must be specified."
        ]
        return result

    execution_context = ExecutionContext(
        resource_type=RESOURCE_TYPE,
        method_name="get",
        method_params={"ctx": ctx, "name": resource_id},
    )

    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def undelete(
    hub,
    ctx,
    unique_id: str,
    project: str = None,
):
    r"""Restores a deleted service account.

    It is not always possible to restore a deleted service account. Use this method only as a last resort.

    After you delete a service account, IAM permanently removes the service account 30 days later. There is no way to
    restore a deleted service account that has been permanently removed.

    The permission 'iam.serviceAccounts.undelete' is required for undeleting resources.

    Although the GCP documentation states that either email or unique_id can be used as resource name, using an email
    results in the following error: "The service account name must be in the following format:
    projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT_UNIQUE_ID}".

    Args:
        unique_id(str):
            The unique, stable numeric ID for the service account.
        project(str, Optional):
            Project ID for this request.
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    if not unique_id:
        result["result"] = False
        result["comment"] = [f"{RESOURCE_TYPE_FULL}#undelete(): unique_id is required"]
        return result

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)
    resource_id = f"projects/{project}/serviceAccounts/{unique_id}"

    execution_context = ExecutionContext(
        resource_type=RESOURCE_TYPE,
        method_name="undelete",
        method_params={"ctx": ctx, "name": resource_id},
    )

    ret = await hub.tool.gcp.generate.generic_exec.execute(execution_context)

    result["comment"] += ret["comment"]
    if not ret["result"]:
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result


async def disable(
    hub,
    ctx,
    project: str = None,
    unique_id: str = None,
    email: str = None,
    resource_id: str = None,
):
    r"""Disables a service account immediately.

    If an application uses the service account to authenticate, that application can no longer call Google APIs or access Google Cloud resources. Existing access tokens for the service account are rejected, and requests for new access tokens will fail.
    To re-enable the service account, use service_account.enable. After you re-enable the service account, its existing access tokens will be accepted, and you can request new access tokens.
    To help avoid unplanned outages, we recommend that you disable the service account before you delete it. Use this method to disable the service account, then wait at least 24 hours and watch for unintended consequences.

    Args:
        project(str, Optional):
            Project ID for this request.
        unique_id(str, Optional):
            The unique, stable numeric ID for the service account.
        email(str, Optional):
            The email address of the service account.
        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.
    """

    def validate(get_ret):
        assert get_ret.get("disabled")

    return await _api_op(
        hub,
        ctx,
        "disable",
        validate,
        project=project,
        unique_id=unique_id,
        email=email,
        resource_id=resource_id,
    )


async def enable(
    hub,
    ctx,
    project: str = None,
    unique_id: str = None,
    email: str = None,
    resource_id: str = None,
):
    r"""Enables a service account that have previously been disabled.

    If the service account is already enabled, then this method has no effect.
    If the service account was disabled by other means — for example, if Google disabled the service account because it was compromised—you cannot use this method to enable the service account.

    Args:
        project(str, Optional):
            Project ID for this request.
        unique_id(str, Optional):
            The unique, stable numeric ID for the service account.
        email(str, Optional):
            The email address of the service account.
        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.
    """

    def validate(get_ret):
        assert "disabled" not in get_ret

    return await _api_op(
        hub,
        ctx,
        "enable",
        validate,
        project=project,
        unique_id=unique_id,
        email=email,
        resource_id=resource_id,
    )


async def _api_op(
    hub,
    ctx,
    api_method: str,
    validate: Callable,
    project: str = None,
    unique_id: str = None,
    email: str = None,
    resource_id: str = None,
):
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }
    if unique_id or email:
        project = hub.tool.gcp.utils.get_project_from_account(ctx, project)
        identifier = unique_id or email
        resource_id = f"projects/{project}/serviceAccounts/{identifier}"
    elif not resource_id:
        result["result"] = False
        result["comment"] = [
            f"{RESOURCE_TYPE_FULL}#{api_method}(): "
            f"either resource_id or unique_id or email should be specified."
        ]
        return result

    async def validate_resource():
        """Validate subsequent get requests return expected output."""
        get_ret = await hub.tool.gcp.generate.generic_exec.execute(
            ExecutionContext(
                resource_type=RESOURCE_TYPE,
                method_name="get",
                method_params={"ctx": ctx, "name": resource_id},
            )
        )
        try:
            assert get_ret["result"]
            validate(get_ret["ret"])
        except AssertionError:
            # return dummy rerun_data to activate reconciliation
            result["rerun_data"] = {"api_method": api_method}
            result["comment"] += get_ret["comment"]
            result["result"] = False
            return result

        result["ret"] = get_ret["ret"]
        return result

    if ctx.get("rerun_data"):
        return await validate_resource()

    execution_context = ExecutionContext(
        resource_type=RESOURCE_TYPE,
        method_name=api_method,
        method_params={"ctx": ctx, "name": resource_id},
    )

    ret = await hub.tool.gcp.generate.generic_exec.execute(execution_context)

    result["comment"] += ret["comment"]
    if not ret["result"]:
        result["result"] = False
        return result

    return await validate_resource()
