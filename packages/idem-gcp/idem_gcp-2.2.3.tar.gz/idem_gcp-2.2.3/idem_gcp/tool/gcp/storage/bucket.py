RESOURCE_TYPE_FULL = f"gcp.storage.bucket"


async def enforce_retention_policy(
    hub,
    ctx,
    result,
    old_is_locked: bool = None,
    new_is_locked: bool = None,
    if_metageneration_match: str = None,
    user_project: str = None,
    resource_id: str = None,
):
    name = result.get("name")

    if new_is_locked is None:
        # not specified in SLS -> no update
        return

    if old_is_locked is None:
        # default GCP value
        old_is_locked = False

    old_is_locked = bool(old_is_locked)
    new_is_locked = bool(new_is_locked)

    if old_is_locked == new_is_locked:
        # no update needed
        return

    if old_is_locked and not new_is_locked:
        result["result"] = False
        result["comment"].append(
            f"Invalid modification of retention_policy.is_locked for {RESOURCE_TYPE_FULL} '{name}' - Retention policy cannot be unlocked once locked"
        )
        return

    if if_metageneration_match is None:
        result["result"] = False
        result["comment"].append(
            f"Locking retention policy for {RESOURCE_TYPE_FULL} '{name}' requires if_metageneration_match SLS property"
        )
        return

    if ctx["test"]:
        result["comment"].append(
            f"Would lock retention policy for {RESOURCE_TYPE_FULL} '{name}'."
        )
        if result["new_state"]["retention_policy"]:
            result["new_state"]["retention_policy"]["is_locked"] = True
        else:
            result["new_state"]["retention_policy"] = {"is_locked": True}
        result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
            result["new_state"]
        )
        return
    else:
        lock_ret = await hub.exec.gcp.storage.bucket.lock_retention_policy(
            ctx=ctx,
            if_metageneration_match=if_metageneration_match,
            resource_id=resource_id,
            user_project=user_project,
        )
        if not lock_ret["result"]:
            result["result"] = False
            result["comment"].append(
                f"Failed to lock retention policy for {RESOURCE_TYPE_FULL} '{name}'."
            )
            result["comment"] += lock_ret["comment"]
            return
        result["comment"].append(
            f"Retention policy locked for {RESOURCE_TYPE_FULL} '{name}'."
        )
