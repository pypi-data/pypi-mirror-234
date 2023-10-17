"""Methods dealing with Cloud KMS IAM policies."""
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List


@dataclass
class AuditLogConfig:
    logType: str
    exemptedMembers: List[str]


@dataclass
class AuditConfig:
    service: str
    auditLogConfigs: List[AuditLogConfig]


@dataclass
class Expr:
    expression: str
    title: str
    description: str = None
    location: str = None


@dataclass
class Binding:
    role: str
    members: List[str]
    condition: Expr = None


@dataclass
class Policy:
    version: int
    bindings: List[Binding]
    auditConfigs: List[AuditConfig] = None
    etag: str = None


async def set_iam_policy(
    hub, ctx, sub, resource: str, policy: Policy, update_mask: str
) -> Dict[str, Any]:
    ret = await sub.setIamPolicy(
        ctx, resource=resource, body={"policy": policy, "updateMask": update_mask}
    )
    return ret


async def get_iam_policy(
    hub, ctx, sub, resource: str, requested_version
) -> Dict[str, Any]:
    ret = await sub.getIamPolicy(
        ctx, resource=resource, __options_requestedPolicyVersion=requested_version
    )
    return ret


# policy_ret = await hub.tool.gcp.policy.get_iam_policy(
#      ctx,
#      hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings,
#      resource_id, 3)

# policy = Policy(version=3,
#                 bindings=[
#                     Binding(role="roles/cloudkms.cryptoKeyDecrypter",
#                             members=["user:dantovska@vmware.com"],
#                             condition=Expr(title="expirable condition",
#                                            expression="request.time < timestamp('2023-10-01T00:00:00.000Z')"))])
# new_policy_ret = await hub.tool.gcp.policy.set_iam_policy(
#     ctx,
#     hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings,
#     resource_id,
#     dataclasses.asdict(policy),
#     None)
