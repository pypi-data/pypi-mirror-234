from typing import Any
from typing import Dict
from typing import List


async def update_named_ports(
    hub,
    ctx,
    current_instance_group: Dict[str, Any],
    new_named_ports: List[Dict[str, Any]],
) -> Dict[str, Any]:
    # Update the updatable named port properties
    result = {"result": False, "comment": []}

    ret = await hub.exec.gcp.compute.instance_group.set_named_ports(
        ctx,
        current_instance_group["resource_id"],
        new_named_ports,
        current_instance_group["fingerprint"],
    )

    if not ret["result"] or not ret["ret"]:
        result["comment"] += ret["comment"]
        return result

    result["result"] = True
    result["ret"] = ret["ret"]

    return result
