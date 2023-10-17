from typing import Any
from typing import Dict
from typing import List


async def update_ip_cidr_range(
    hub,
    ctx,
    current_subnetwork: Dict[str, Any],
    new_ip_cidr_range: List[Dict[str, Any]],
) -> Dict[str, Any]:
    resource_id = current_subnetwork.get("resource_id")

    return await hub.exec.gcp.compute.subnetwork.update_ip_cidr_range(
        ctx,
        new_ip_cidr_range,
        current_subnetwork.get("project"),
        current_subnetwork.get("region"),
        current_subnetwork,
        resource_id,
    )
