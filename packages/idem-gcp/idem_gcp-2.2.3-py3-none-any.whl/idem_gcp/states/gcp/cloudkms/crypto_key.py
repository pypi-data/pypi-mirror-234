"""State module for managing Cloud Key Management Service crypto keys."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]
RESOURCE_TYPE = "cloudkms.crypto_key"
RESOURCE_TYPE_FULL = "cloudkms.projects.locations.key_rings.crypto_keys"
GCP_RESOURCE_TYPE_FULL = "gcp.cloudkms.crypto_key"


async def present(
    hub,
    ctx,
    name: str,
    crypto_key_id: str = None,
    project_id: str = None,
    location_id: str = None,
    key_ring_id: str = None,
    primary: make_dataclass(
        "CryptoKeyVersion",
        [
            ("name", str),
            ("state", str, field(default=None)),
            ("protection_level", str, field(default=None)),
            ("algorithm", str, field(default=None)),
            (
                "attestation",
                make_dataclass(
                    "KeyOperationAttestation",
                    [
                        ("format", str, field(default=None)),
                        ("content", str, field(default=None)),
                        (
                            "cert_chains",
                            make_dataclass(
                                "CertificateChains",
                                [
                                    ("cavium_certs", List[str], field(default=None)),
                                    (
                                        "google_card_certs",
                                        List[str],
                                        field(default=None),
                                    ),
                                    (
                                        "google_partition_certs",
                                        List[str],
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
                field(default=None),
            ),
            ("create_time", str, field(default=None)),
            ("generate_time", str, field(default=None)),
            ("destroy_time", str, field(default=None)),
            ("destroy_event_time", str, field(default=None)),
            ("import_job", str, field(default=None)),
            ("import_time", str, field(default=None)),
            ("import_failure_reason", str, field(default=None)),
            (
                "external_protection_level_options",
                make_dataclass(
                    "ExternalProtectionLevelOptions",
                    [
                        ("external_key_uri", str, field(default=None)),
                        ("ekm_connection_key_path", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("reimport_eligible", bool, field(default=None)),
        ],
    ) = None,
    purpose: str = None,
    create_time: str = None,
    next_rotation_time: str = None,
    version_template: make_dataclass(
        "CryptoKeyVersionTemplate",
        [
            ("protection_level", str, field(default=None)),
            ("algorithm", str, field(default=None)),
        ],
    ) = None,
    labels: Dict[str, str] = None,
    import_only: bool = None,
    destroy_scheduled_duration: str = None,
    crypto_key_backend: str = None,
    rotation_period: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    r"""Create or update a `CryptoKey`_ within a `KeyRing`_.

    `CryptoKey.purpose`_ and `CryptoKey.version_template.algorithm`_ are required for a new `CryptoKey`_.

    Args:
        name(str):
            Idem name.

        crypto_key_id(str, Optional):
            Crypto key id.

        project_id(str, Optional):
            Project Id of the new crypto key.

        location_id(str, Optional):
            Location Id of the new crypto key.

        key_ring_id(str, Optional):
            Keyring Id of the new crypto key.

        primary(Dict[str, Any], Optional):
            A copy of the "primary" CryptoKeyVersion that will be used by cryptoKeys.encrypt when this
            CryptoKey is given in EncryptRequest.name. Keys with purpose ENCRYPT_DECRYPT may have a primary. For other keys,
            this field will be omitted. To update the primary key provide only `primary.name = new_resource_id`. All
            other CryptoKeyVersion are output only.

            * name(str, Optional):
                Output only. The resource name for this CryptoKeyVersion in the format `projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*`.

            * state(str, Optional):
                The current state of the CryptoKeyVersion.
                Enum type. Allowed values:
                    "CRYPTO_KEY_VERSION_STATE_UNSPECIFIED"
                    "PENDING_GENERATION"
                    "ENABLED"
                    "DISABLED"
                    "DESTROYED"
                    "DESTROY_SCHEDULED"
                    "PENDING_IMPORT"
                    "IMPORT_FAILED"
                    "GENERATION_FAILED"
                    "PENDING_EXTERNAL_DESTRUCTION"
                    "EXTERNAL_DESTRUCTION_FAILED"

            * protection_level(str, Optional):
                Output only. The ProtectionLevel describing how crypto operations are performed with this CryptoKeyVersion.
                Enum type. Allowed values:
                    "PROTECTION_LEVEL_UNSPECIFIED"
                    "SOFTWARE"
                    "HSM"
                    "EXTERNAL"
                    "EXTERNAL_VPC"

            * algorithm(str, Optional):
                Output only. The CryptoKeyVersionAlgorithm that this CryptoKeyVersion supports.
                Enum type. Allowed values:
                    "CRYPTO_KEY_VERSION_ALGORITHM_UNSPECIFIED"
                    "GOOGLE_SYMMETRIC_ENCRYPTION"
                    "RSA_SIGN_PSS_2048_SHA256"
                    "RSA_SIGN_PSS_3072_SHA256"
                    "RSA_SIGN_PSS_4096_SHA256"
                    "RSA_SIGN_PSS_4096_SHA512"
                    "RSA_SIGN_PKCS1_2048_SHA256"
                    "RSA_SIGN_PKCS1_3072_SHA256"
                    "RSA_SIGN_PKCS1_4096_SHA256"
                    "RSA_SIGN_PKCS1_4096_SHA512"
                    "RSA_SIGN_RAW_PKCS1_2048"
                    "RSA_SIGN_RAW_PKCS1_3072"
                    "RSA_SIGN_RAW_PKCS1_4096"
                    "RSA_DECRYPT_OAEP_2048_SHA256"
                    "RSA_DECRYPT_OAEP_3072_SHA256"
                    "RSA_DECRYPT_OAEP_4096_SHA256"
                    "RSA_DECRYPT_OAEP_4096_SHA512"
                    "RSA_DECRYPT_OAEP_2048_SHA1"
                    "RSA_DECRYPT_OAEP_3072_SHA1"
                    "RSA_DECRYPT_OAEP_4096_SHA1"
                    "EC_SIGN_P256_SHA256"
                    "EC_SIGN_P384_SHA384"
                    "EC_SIGN_SECP256K1_SHA256"
                    "HMAC_SHA256"
                    "HMAC_SHA1"
                    "HMAC_SHA384"
                    "HMAC_SHA512"
                    "HMAC_SHA224"
                    "EXTERNAL_SYMMETRIC_ENCRYPTION"

            * attestation(Dict[str, Any], Optional):
                Output only. Statement that was generated and signed by the HSM at key creation time.
                Use this statement to verify attributes of the key as stored on the HSM, independently of Google.
                Only provided for key versions with protection_level HSM.

                * format(str, Optional):
                    Output only. The format of the attestation data.
                    Enum type. Allowed values:
                        "ATTESTATION_FORMAT_UNSPECIFIED"
                        "CAVIUM_V1_COMPRESSED"
                        "CAVIUM_V2_COMPRESSED"

                * content(str, Optional):
                    Output only. The attestation data provided by the HSM when the key operation was performed.

                * cert_chains(Dict[str, Any], Optional):
                    Output only. The certificate chains needed to validate the attestation.
                    Certificate chains needed to verify the attestation. Certificates in chains are PEM-encoded
                    and are ordered based on https://tools.ietf.org/html/rfc5246#section-7.4.2.

                    * cavium_certs(list[str], Optional):
                        Cavium certificate chain corresponding to the attestation.

                    * google_card_certs(list[str], Optional):
                        Google card certificate chain corresponding to the attestation.

                    * google_partition_certs(list[str], Optional):
                        Google partition certificate chain corresponding to the attestation.

            * create_time(str, Optional):
                Output only. The time at which this CryptoKeyVersion was created.

            * generate_time(str, Optional):
                Output only. The time this CryptoKeyVersion's key material was generated.

            * destroy_time(str, Optional):
                Output only. The time this CryptoKeyVersion's key material is scheduled for destruction. Only present if state is DESTROY_SCHEDULED.

            * destroy_event_time(str, Optional):
                Output only. The time this CryptoKeyVersion's key material was destroyed. Only present if state is DESTROYED.

            * import_job(str, Optional):
                Output only. The name of the ImportJob used in the most recent import of this CryptoKeyVersion.
                Only present if the underlying key material was imported.

            * import_time(str, Optional):
                Output only. The time at which this CryptoKeyVersion's key material was most recently imported.

            * import_failure_reason(str, Optional):
                Output only. The root cause of the most recent import failure. Only present if state is IMPORT_FAILED.

            * external_protection_level_options(Dict[str, Any], Optional):
                ExternalProtectionLevelOptions stores a group of additional fields for configuring a CryptoKeyVersion that
                are specific to the EXTERNAL protection level and EXTERNAL_VPC protection levels.
                * external_key_uri(str, Optional):
                    The URI for an external resource that this CryptoKeyVersion represents.
                * ekm_connection_key_path(str, Optional):
                    The path to the external key material on the EKM when using EkmConnection e.g., "v0/my/key". Set this field instead of external_key_uri when using an EkmConnection.

            * reimport_eligible(bool, Optional):
                Output only. Whether or not this key version is eligible for reimport, by being specified as a target in ImportCryptoKeyVersionRequest.crypto_key_version.

        purpose(str, Optional):
            Immutable. The immutable purpose of this CryptoKey.

        create_time(str, Optional):
            Output only. The time at which this CryptoKey was created. A timestamp in RFC3339 UTC "Zulu" format, with
            nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and
            "2014-10-02T15:01:23.045123456Z".

        next_rotation_time(str, Optional):
            At nextRotationTime, the Key Management Service will automatically:

            - Create a new version of this CryptoKey.
            - Mark the new version as primary.

            Key rotations performed manually via cryptoKeyVersions.create and cryptoKeys.updatePrimaryVersion do not
            affect nextRotationTime. Keys with purpose ENCRYPT_DECRYPT support automatic rotation. For other keys, this
            field must be omitted. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine
            fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        version_template(Dict[str, Any], Optional):
            A template describing settings for new CryptoKeyVersion instances. The properties of new CryptoKeyVersion
            instances created by either cryptoKeyVersions.create or auto-rotation are controlled by this template.

            * algorithm(str, Optional):
                "Required. Algorithm to use when creating a CryptoKeyVersion based on this template.
                For backwards compatibility, GOOGLE_SYMMETRIC_ENCRYPTION is implied if both this field is omitted and CryptoKey.purpose is ENCRYPT_DECRYPT."
                Enum type. Allowed values:
                    "CRYPTO_KEY_VERSION_ALGORITHM_UNSPECIFIED"
                    "GOOGLE_SYMMETRIC_ENCRYPTION"
                    "RSA_SIGN_PSS_2048_SHA256"
                    "RSA_SIGN_PSS_3072_SHA256"
                    "RSA_SIGN_PSS_4096_SHA256"
                    "RSA_SIGN_PSS_4096_SHA512"
                    "RSA_SIGN_PKCS1_2048_SHA256"
                    "RSA_SIGN_PKCS1_3072_SHA256"
                    "RSA_SIGN_PKCS1_4096_SHA256"
                    "RSA_SIGN_PKCS1_4096_SHA512"
                    "RSA_SIGN_RAW_PKCS1_2048"
                    "RSA_SIGN_RAW_PKCS1_3072"
                    "RSA_SIGN_RAW_PKCS1_4096"
                    "RSA_DECRYPT_OAEP_2048_SHA256"
                    "RSA_DECRYPT_OAEP_3072_SHA256"
                    "RSA_DECRYPT_OAEP_4096_SHA256"
                    "RSA_DECRYPT_OAEP_4096_SHA512"
                    "RSA_DECRYPT_OAEP_2048_SHA1"
                    "RSA_DECRYPT_OAEP_3072_SHA1"
                    "RSA_DECRYPT_OAEP_4096_SHA1"
                    "EC_SIGN_P256_SHA256"
                    "EC_SIGN_P384_SHA384"
                    "EC_SIGN_SECP256K1_SHA256"
                    "HMAC_SHA256"
                    "HMAC_SHA1"
                    "HMAC_SHA384"
                    "HMAC_SHA512"
                    "HMAC_SHA224"
                    "EXTERNAL_SYMMETRIC_ENCRYPTION"
            * protection_level(str, Optional):
                ProtectionLevel to use when creating a CryptoKeyVersion based on this template. Immutable. Defaults to SOFTWARE.
                Enum type. Allowed values:
                    "PROTECTION_LEVEL_UNSPECIFIED"
                    "SOFTWARE"
                    "HSM"
                    "EXTERNAL"
                    "EXTERNAL_VPC"

        labels(Dict[str, str], Optional):
            Labels with user-defined metadata. For more information, see `Labeling Keys`_.

        import_only(bool, Optional):
            Immutable. Whether this key may contain imported versions only.

        destroy_scheduled_duration(str, Optional):
            Immutable. The period of time that versions of this key spend in the DESTROY_SCHEDULED state before
            transitioning to DESTROYED. If not specified at creation time, the default duration is 24 hours. A duration
            in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        crypto_key_backend(str, Optional):
            Immutable. The resource name of the backend environment where the key material for all CryptoKeyVersions
            associated with this `CryptoKey`_ reside and where all related cryptographic operations are performed. Only
            applicable if `CryptoKeyVersions`_ have a `ProtectionLevel`_ of
            [EXTERNAL_VPC][CryptoKeyVersion.ProtectionLevel.EXTERNAL_VPC], with the resource name in the format
            `projects/\\*/locations/\\*/ekmConnections/\\*`. Note, this list is non-exhaustive and may apply to additional
            `ProtectionLevels`_ in the future.

        rotation_period(str, Optional):
            next_rotation_time will be advanced by this period when the service automatically rotates a key.
            Must be at least 24 hours and at most 876,000 hours.

            If rotation_period is set, next_rotation_time must also be set. Keys
            with purpose ENCRYPT_DECRYPT support automatic rotation. For other keys, this field must be omitted.

            A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        resource_id(str, Optional): Idem resource id. Formatted as

            `projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}`

    .. _CryptoKey: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKey
    .. _KeyRing: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings#KeyRing
    .. _CryptoKey.purpose: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKey.FIELDS.purpose
    .. _CryptoKey.version_template.algorithm: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKeyVersionTemplate.FIELDS.algorithm
    .. _Labeling Keys: https://cloud.google.com/kms/docs/labeling-keys
    .. _CryptoKeyVersions: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion
    .. _ProtectionLevel: https://cloud.google.com/kms/docs/reference/rest/v1/ProtectionLevel
    .. _ProtectionLevels: https://cloud.google.com/kms/docs/reference/rest/v1/ProtectionLevel

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            crypto_key_present:
              gcp.cloudkms.crypto_key.present:
              - primary:
                  name: projects/project-name/locations/us-east1/keyRings/key-ring/cryptoKeys/key-1/cryptoKeyVersions/1
              - purpose: ENCRYPT_DECRYPT
              - labels:
                  lbl_key_1: lbl-value-1
              - version_template:
                  algorithm: GOOGLE_SYMMETRIC_ENCRYPTION
                  protection_level: SOFTWARE
              - destroy_scheduled_duration: 86400s
              - rotation_period: 31500001s
              - next_rotation_time: "2024-10-02T15:01:23Z"
              - resource_id: projects/project-name/locations/us-east1/keyRings/key-ring/cryptoKeys/key-1
              - project_id: project-name
              - location_id: us-east1
              - key_ring_id: key-ring
              - crypto_key_id: key-1
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    get_resource_only_with_resource_id = hub.OPT.idem.get(
        "get_resource_only_with_resource_id", False
    )

    if hub.tool.gcp.resource_prop_utils.properties_mismatch_resource_id(
        RESOURCE_TYPE_FULL,
        resource_id,
        {
            "project_id": project_id,
            "location_id": location_id,
            "key_ring_id": key_ring_id,
            "crypto_key_id": crypto_key_id,
        },
    ):
        result["comment"].append(
            hub.tool.gcp.comment_utils.properties_mismatch_resource_id_comment(
                RESOURCE_TYPE_FULL, name
            )
        )

    if resource_id:
        old_get_ret = await hub.exec.gcp.cloudkms.crypto_key.get(
            ctx, resource_id=resource_id
        )

        if not old_get_ret["result"] or (
            not old_get_ret["ret"] and get_resource_only_with_resource_id
        ):
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        result["old_state"] = old_get_ret["ret"]
    elif not get_resource_only_with_resource_id:
        resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
            RESOURCE_TYPE_FULL,
            {
                "project_id": project_id,
                "location_id": location_id,
                "key_ring_id": key_ring_id,
                "crypto_key_id": crypto_key_id,
            },
        )
        old_get_ret = await hub.exec.gcp.cloudkms.crypto_key.get(
            ctx, resource_id=resource_id
        )

        if not old_get_ret["result"]:
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        if old_get_ret["ret"]:
            result["old_state"] = old_get_ret["ret"]

    if not result["old_state"]:
        resource_body = {
            "purpose": purpose,
            "next_rotation_time": next_rotation_time,
            "version_template": version_template,
            "labels": labels,
            "import_only": import_only,
            "destroy_scheduled_duration": destroy_scheduled_duration,
            "crypto_key_backend": crypto_key_backend,
            "rotation_period": rotation_period,
        }
    else:
        resource_body = {
            "next_rotation_time": next_rotation_time,
            "version_template": version_template,
            "labels": hub.tool.gcp.cloudkms.patch.merge_labels(
                labels, result["old_state"].get("labels")
            ),
            "rotation_period": rotation_period,
        }

    resource_body = {k: v for (k, v) in resource_body.items() if v is not None}

    if result["old_state"]:
        resource_id = result["old_state"].get("resource_id", None)
        update_mask = hub.tool.gcp.cloudkms.patch.calc_update_mask(
            resource_body, result["old_state"]
        )
        if (
            primary
            and primary.get("name")
            and primary["name"]
            != (result["old_state"].get("primary") or {}).get("name")
        ):
            update_primary_version = True
        else:
            update_primary_version = False

        if ctx["test"]:
            if update_mask or update_primary_version:
                result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                    {**result["old_state"], **resource_body}
                )
                result["comment"].append(
                    hub.tool.gcp.comment_utils.would_update_comment(
                        GCP_RESOURCE_TYPE_FULL, resource_id
                    )
                )
            else:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.up_to_date_comment(
                        GCP_RESOURCE_TYPE_FULL, resource_id
                    )
                )
            return result

        els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
            RESOURCE_TYPE_FULL, resource_id
        )
        if (
            els.get("project_id") != project_id
            or els.get("location_id") != location_id
            or els.get("key_ring_id") != key_ring_id
            or els.get("crypto_key_id") != crypto_key_id
        ):
            result["result"] = False
            result["comment"].append(
                hub.tool.gcp.comment_utils.non_updatable_properties_comment(
                    GCP_RESOURCE_TYPE_FULL,
                    resource_id,
                    ["project_id", "location_id", "key_ring_id", "crypto_key_id"],
                )
            )
            return result

        if update_mask:
            update_ret = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.patch(
                ctx, name_=resource_id, updateMask=update_mask, body=resource_body
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] += update_ret["comment"]
                return result

            result["new_state"] = {
                "name": name,
                "project_id": project_id,
                "location_id": location_id,
                "key_ring_id": key_ring_id,
                "crypto_key_id": crypto_key_id,
                **update_ret["ret"],
            }

        if update_primary_version:
            els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
                "cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions",
                primary["name"],
            )
            update_version_ret = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.updatePrimaryVersion(
                ctx,
                name_=resource_id,
                body={"cryptoKeyVersionId": els["crypto_key_version_id"]},
            )
            if not update_version_ret["result"]:
                result["result"] = False
                result["comment"] += update_version_ret["comment"]
                return result

            result["new_state"] = {
                "name": name,
                "project_id": project_id,
                "location_id": location_id,
                "key_ring_id": key_ring_id,
                "crypto_key_id": crypto_key_id,
                "primary": update_version_ret["ret"]["primary"],
            }

        if update_mask or update_primary_version:
            result["comment"].append(
                hub.tool.gcp.comment_utils.update_comment(
                    GCP_RESOURCE_TYPE_FULL, resource_id
                )
            )
        else:
            result["comment"].append(
                hub.tool.gcp.comment_utils.up_to_date_comment(
                    GCP_RESOURCE_TYPE_FULL, resource_id
                )
            )
        return result

    else:
        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    GCP_RESOURCE_TYPE_FULL, name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                {
                    "resource_id": resource_id,
                    "name": name,
                    "project_id": project_id,
                    "location_id": location_id,
                    "key_ring_id": key_ring_id,
                    "crypto_key_id": crypto_key_id,
                    **resource_body,
                }
            )
            return result

        create_ret = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.create(
            ctx,
            parent=hub.tool.gcp.resource_prop_utils.construct_resource_id(
                "cloudkms.projects.locations.key_rings",
                {
                    "project_id": project_id,
                    "location_id": location_id,
                    "key_ring_id": key_ring_id,
                },
            ),
            body=resource_body,
            crypto_key_id=crypto_key_id,
            skip_initial_version_creation=False,
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] += create_ret["comment"]
            return result
        result["comment"].append(
            hub.tool.gcp.comment_utils.create_comment(
                GCP_RESOURCE_TYPE_FULL, resource_id
            )
        )
        result["new_state"] = {
            "name": name,
            "project_id": project_id,
            "location_id": location_id,
            "key_ring_id": key_ring_id,
            "crypto_key_id": crypto_key_id,
            **create_ret["ret"],
        }
        result["old_state"] = {}
        return result


async def absent(hub, ctx, name: str) -> Dict[str, Any]:
    """Absent is not supported for this resource.

    Args:
        name(str):
            Idem name

    Returns:
        .. code-block:: json

            {
                "result": False,
                "comment": "...",
                "old_state": None,
                "new_state": None,
            }
    """
    return {
        "name": name,
        "result": False,
        "comment": [
            hub.tool.gcp.comment_utils.no_resource_delete_comment(
                GCP_RESOURCE_TYPE_FULL
            )
        ],
        "old_state": None,
        "new_state": None,
    }


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieve the list of available crypto keys.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.cloudkms.crypto_key
    """
    result = {}

    locations = await hub.exec.gcp.cloudkms.location.list(
        ctx, project=ctx.acct.project_id
    )
    if not locations["result"]:
        hub.log.warning(
            f"Could not list gcp.cloudkms.crypto_key in {ctx.acct.project_id} {locations['comment']}"
        )
        return {}

    for location in locations["ret"]:
        key_rings = await hub.exec.gcp.cloudkms.key_ring.list(
            ctx, location=location["resource_id"]
        )
        if not key_rings["result"]:
            hub.log.warning(
                f"Could not list gcp.cloudkms.key_ring in {location['location_id']} {key_rings['comment']}"
            )
        else:
            for key_ring in key_rings["ret"]:
                crypto_keys = await hub.exec.gcp.cloudkms.crypto_key.list(
                    ctx, key_ring=key_ring["resource_id"]
                )
                if not crypto_keys["result"]:
                    hub.log.debug(
                        f"Could not describe gcp.cloudkms.crypto_key in {key_ring['resource_id']} {key_rings['comment']}"
                    )
                else:
                    for crypto_key in crypto_keys["ret"]:
                        resource_id = crypto_key["resource_id"]
                        result[resource_id] = {
                            "gcp.cloudkms.crypto_key.present": [
                                {parameter_key: parameter_value}
                                for parameter_key, parameter_value in crypto_key.items()
                            ]
                        }
                        els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
                            RESOURCE_TYPE_FULL,
                            resource_id,
                        )
                        p = result[resource_id]["gcp.cloudkms.crypto_key.present"]
                        p.append({"project_id": els["project_id"]})
                        p.append({"location_id": els["location_id"]})
                        p.append({"key_ring_id": els["key_ring_id"]})
                        p.append({"crypto_key_id": els["crypto_key_id"]})

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
