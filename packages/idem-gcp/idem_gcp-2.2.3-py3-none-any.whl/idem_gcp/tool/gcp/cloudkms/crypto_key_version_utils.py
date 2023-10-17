"""Utility functions for crypto key version resources."""
import copy
import os
from typing import Any
from typing import Dict

from cryptography.hazmat import backends
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import keywrap
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


def to_state(hub, state: Dict[str, Any]) -> Dict[str, Any]:
    """`state` is reserved in Idem and can be a parameter name in `present`.

    This method returns a copy of the original new/old state to get rid of NamespacedDict
    and replaces `state` with `key_state`. GCP `name` is translated to Idem `resource_id`.

    Args:
        state: new_state or old_state formatted variable

    Returns:
        Dict[str, Any]
    """
    result = copy.copy(state)
    if "state" in result:
        key_state = result["state"]
        del result["state"]
        result["key_state"] = key_state

    if "resource_id" in result:
        els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
            "cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions",
            result["resource_id"],
        )
        result["crypto_key_version_id"] = els["crypto_key_version_id"]
    return result


def wrap_key(hub, formatted_key: bytes, import_job_pub_key: str) -> bytes:
    """
    Generates and imports local key material to Cloud KMS.

    Args:
        formatted_key (bytes): Key material.
        import_job_pub_key (str): PEM encoded import job public key.

    Returns:
        bytes
    """
    # Generate a temporary 32-byte key for AES-KWP and wrap the key material.
    kwp_key = os.urandom(32)
    wrapped_target_key = keywrap.aes_key_wrap_with_padding(
        kwp_key, formatted_key, backends.default_backend()
    )

    # Retrieve the public key from the import job.
    import_job_pub = serialization.load_pem_public_key(
        bytes(import_job_pub_key, "UTF-8"), backends.default_backend()
    )

    # Wrap the KWP key using the import job key.
    wrapped_kwp_key = import_job_pub.encrypt(
        kwp_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None,
        ),
    )
    return wrapped_kwp_key + wrapped_target_key


async def get_import_key_if_eligible(
    hub,
    ctx,
    has_key_material: bool,
    has_algorithm: str,
    import_job: str,
    crypto_key_version_state: str,
) -> Dict[str, Any]:
    r"""Retrieves public key from an import job if key_material is provided.

     This method checks that import job is ACTIVE and `CryptoKeyVersion`_ be in `DESTROYED`_ or `IMPORT_FAILED`_ state.
     The key material and algorithm must match the previous `CryptoKeyVersion`_ exactly if the `CryptoKeyVersion`_ has
     ever contained key material.

    .. _CryptoKeyVersion: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion
    .. _DESTROYED: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion.CryptoKeyVersionState.ENUM_VALUES.DESTROYED
    .. _IMPORT_FAILED: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion.CryptoKeyVersionState.ENUM_VALUES.IMPORT_FAILED

    Args:
        has_key_material(bool): Required. Key material for import is available.
        has_algorithm(bool): Required but may evaluate to None. Algorithm is provided.
        import_job(str): Required but may evaluate to None. Import job Idem resource_id.
        crypto_key_version_state(str):
            Required but may evaluate to None. State of the crypto_key_version if importing into old instance.

    Returns:
        Dict[str, Any]
    """
    result = {"result": True, "comment": [], "ret": None}
    if not has_key_material:
        return result
    if not has_algorithm or not import_job:
        result["result"] = False
        result["comment"].append(
            f"Import will be attempted because key_material was provided but either algorithm or import_job is not specified."
        )
        return result
    if crypto_key_version_state and crypto_key_version_state not in [
        "DESTROYED",
        "IMPORT_FAILED",
    ]:
        result["result"] = False
        result["comment"].append(
            f"Reimport will be attempted because key_material was provided but crypto_key_version is not in the proper state."
        )
        return result

    import_job_ret = await hub.exec.gcp.cloudkms.import_job.get(
        ctx, resource_id=import_job
    )

    if not import_job_ret["result"] or not import_job_ret["ret"]:
        result["result"] = False
        result["comment"] += import_job_ret["comment"]
        return result

    import_job_resource = import_job_ret["ret"]

    if import_job_resource["state"] != "ACTIVE":
        result["result"] = False
        result["comment"] += (
            f"Import job {import_job} should be in state ACTIVE but current state is {import_job_resource['state']}",
        )
        return result

    result["ret"] = import_job_resource["public_key"]["pem"]
    return result
