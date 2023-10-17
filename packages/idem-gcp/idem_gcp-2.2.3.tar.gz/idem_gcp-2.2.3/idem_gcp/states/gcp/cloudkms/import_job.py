"""State module for managing Cloud Key Management Service import job."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]
RESOURCE_TYPE = "cloudkms.import_jobs"
RESOURCE_TYPE_FULL = "cloudkms.projects.locations.key_rings.import_jobs"
GCP_RESOURCE_TYPE_FULL = "gcp.cloudkms.import_jobs"


async def present(
    hub,
    ctx,
    name: str,
    import_method: str,
    protection_level: str,
    import_job_id: str = None,
    project_id: str = None,
    location_id: str = None,
    key_ring_id: str = None,
    create_time: str = None,
    generate_time: str = None,
    expire_time: str = None,
    expire_event_time: str = None,
    job_state: str = None,
    public_key: str = None,
    attestation: make_dataclass(
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
    ) = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Create a new `ImportJob`_ within a `KeyRing`_.

    Args:
        name(str):
            Idem name.

        import_job_id(str, Optional):
            Import job id. It must be unique within a KeyRing and match the regular expression ``[a-zA-Z0-9_-]{1,63}``

        project_id(str, Optional):
            Project Id of the new crypto key.

        location_id(str, Optional):
            Location Id of the new crypto key.

        key_ring_id(str, Optional):
            Keyring Id of the new crypto key.

        import_method(str):
            Immutable. The wrapping method to be used for incoming key material. See `ImportMethod`_.

        protection_level(str):
            Immutable. The protection level of the `ImportJob`_. This must match the `protectionLevel`_ of the
            `versionTemplate`_ on the `CryptoKey`_ you attempt to import into.

        create_time(str, Optional):
            Output only. The time at which this `ImportJob`_ was created.

            A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits.
            Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        generate_time(str, Optional):
            Output only. The time this `ImportJob`_'s key material was generated.

            A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits.
            Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        expire_time(str, Optional):
            Output only. The time at which this `ImportJob`_ is scheduled for expiration and can no longer be used to
            import key material.

            A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits.
            Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        expire_event_time(str, Optional):
            Output only. The time this `ImportJob`_ expired. Only present if `state`_ is `EXPIRED`_.

            A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits.
            Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        job_state(str, Optional):
            Output only. The current state of the `ImportJob`_, indicating if it can be used.

        public_key(str, Optional):
            Output only. The public key with which to wrap key material prior to import. Only returned if `state`_ is
             `ACTIVE`_.

        attestation(Dict[str, Any], Optional):
            Output only. Statement that was generated and signed by the key creator (for example, an HSM) at key
            creation time. Use this statement to verify attributes of the key as stored on the HSM, independently
            of Google. Only present if the chosen ImportMethod is one with a protection level of HSM.

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

        resource_id(str, Optional): Idem resource id. Formatted as

            `projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/importJobs/{import_job_id}`

    .. _ImportJob: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.importJobs#ImportJob
    .. _KeyRing: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings#KeyRing
    .. _Labeling Keys: https://cloud.google.com/kms/docs/labeling-keys
    .. _ProtectionLevel: https://cloud.google.com/kms/docs/reference/rest/v1/ProtectionLevel
    .. _ImportMethod: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.importJobs#ImportMethod
    .. _CryptoKey: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKey
    .. _versionTemplate: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKey.FIELDS.version_template
    .. _protectionLevel: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKeyVersionTemplate.FIELDS.protection_level
    .. _state: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.importJobs#ImportJob.FIELDS.state
    .. _EXPIRED: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.importJobs#ImportJobState.ENUM_VALUES.EXPIRED
    .. _ACTIVE: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.importJobs#ImportJobState.ENUM_VALUES.ACTIVE
    .. _ImportMethod: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.importJobs#ImportMethod
    .. _HSM: https://cloud.google.com/kms/docs/reference/rest/v1/ProtectionLevel#ENUM_VALUES.HSM

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            import_job_present:
              gcp.cloudkms.import_job.present:
                - import_method: RSA_OAEP_4096_SHA256
                - protection_level: SOFTWARE
                - project_id: project-name
                - location_id: us-east1
                - key_ring_id: key-ring-id
                - import_job_id: import-job-id

    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    if hub.tool.gcp.resource_prop_utils.properties_mismatch_resource_id(
        RESOURCE_TYPE_FULL,
        resource_id,
        {
            "project_id": project_id,
            "location_id": location_id,
            "key_ring_id": key_ring_id,
            "import_job_id": import_job_id,
        },
    ):
        result["comment"].append(
            hub.tool.gcp.comment_utils.properties_mismatch_resource_id_comment(
                RESOURCE_TYPE_FULL, name
            )
        )

    get_resource_only_with_resource_id = hub.OPT.idem.get(
        "get_resource_only_with_resource_id", False
    )
    if resource_id:
        old_get_ret = await hub.exec.gcp.cloudkms.import_job.get(
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
                "import_job_id": import_job_id,
            },
        )
        old_get_ret = await hub.exec.gcp.cloudkms.import_job.get(
            ctx, resource_id=resource_id
        )

        if not old_get_ret["result"]:
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        if old_get_ret["ret"]:
            result["old_state"] = old_get_ret["ret"]

    if result["old_state"]:
        resource_id = result["old_state"].get("resource_id", None)
        els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
            RESOURCE_TYPE_FULL, resource_id
        )
        if project_id and location_id and key_ring_id and import_job_id:
            if (
                els.get("project_id") != project_id
                or els.get("location_id") != location_id
                or els.get("key_ring_id") != key_ring_id
                or els.get("import_job_id") != import_job_id
            ):
                result["result"] = False
                result["comment"].append(
                    hub.tool.gcp.comment_utils.non_updatable_properties_comment(
                        "gcp.cloudkms.import_job",
                        resource_id,
                        ["project_id", "location_id", "key_ring_id", "import_job_id"],
                    )
                )
                return result

        if (
            result["old_state"].get("import_method") != import_method
            or result["old_state"].get("protection_level") != protection_level
        ):
            result["result"] = False
            result["comment"].append(
                hub.tool.gcp.comment_utils.no_resource_update_comment(
                    "gcp.cloudkms.import_job", resource_id
                )
            )
        else:
            result["comment"].append(
                hub.tool.gcp.comment_utils.already_exists_comment(
                    "gcp.cloudkms.import_job", resource_id
                )
            )
            result["new_state"] = result["old_state"]

        return result

    resource_body = {
        "importMethod": import_method,
        "protectionLevel": protection_level,
    }

    if ctx["test"]:
        result["comment"].append(
            hub.tool.gcp.comment_utils.would_create_comment(
                "gcp.cloudkms.import_job", resource_id
            )
        )
        result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
            {
                "resource_id": resource_id,
                "name": name,
                "project_id": project_id,
                "location_id": location_id,
                "key_ring_id": key_ring_id,
                "import_job_id": import_job_id,
                **resource_body,
            }
        )
        return result

    create_ret = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.import_jobs.create(
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
        import_job_id=import_job_id,
    )

    if not create_ret["result"]:
        result["result"] = False
        result["comment"] += create_ret["comment"]
        return result
    result["comment"].append(
        hub.tool.gcp.comment_utils.create_comment(
            "gcp.cloudkms.import_job", resource_id
        )
    )
    result["new_state"] = {
        "name": name,
        "project_id": project_id,
        "location_id": location_id,
        "key_ring_id": key_ring_id,
        "import_job_id": import_job_id,
        **create_ret["ret"],
    }
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
                "gcp.cloudkms.import_job"
            )
        ],
        "old_state": None,
        "new_state": None,
    }


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieve the list of available import jobs.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.cloudkms.import_job
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
                import_jobs = await hub.exec.gcp.cloudkms.import_job.list(
                    ctx, key_ring=key_ring["resource_id"]
                )
                if not import_jobs["result"]:
                    hub.log.debug(
                        f"Could not describe gcp.cloudkms.import_job in {key_ring['resource_id']} {key_rings['comment']}"
                    )
                else:
                    for import_job in import_jobs["ret"]:
                        resource_id = import_job["resource_id"]
                        result[resource_id] = {
                            "gcp.cloudkms.import_job.present": [
                                {parameter_key: parameter_value}
                                if parameter_key != "state"
                                else {"job_state": parameter_value}
                                for parameter_key, parameter_value in import_job.items()
                            ]
                        }
                        els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
                            RESOURCE_TYPE_FULL,
                            resource_id,
                        )
                        p = result[resource_id]["gcp.cloudkms.import_job.present"]
                        p.append({"project_id": els["project_id"]})
                        p.append({"location_id": els["location_id"]})
                        p.append({"key_ring_id": els["key_ring_id"]})
                        p.append({"import_job_id": els["import_job_id"]})

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
