"""State module for managing Cloud Key Management Service crypto keys."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict

__contracts__ = ["resource"]
RESOURCE_TYPE = "cloudkms.crypto_key_versions"
RESOURCE_TYPE_FULL = (
    "cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions"
)
GCP_RESOURCE_TYPE_FULL = "gcp.cloudkms.crypto_key_versions"


async def present(
    hub,
    ctx,
    name: str,
    crypto_key_version_id: str = None,
    project_id: str = None,
    location_id: str = None,
    key_ring_id: str = None,
    crypto_key_id: str = None,
    key_state: str = None,
    algorithm: str = None,
    import_job: str = None,
    external_protection_level_options: make_dataclass(
        "ExternalProtectionLevelOptions",
        [
            ("external_key_uri", str, field(default=None)),
            ("ekm_connection_key_path", str, field(default=None)),
        ],
    ) = None,
    resource_id: str = None,
    key_material: str = None,
) -> Dict[str, Any]:
    """Create or update a `CryptoKeyVersion`_ within a `CryptoKey`_.

    Args:
        name(str):
            Idem name.

        crypto_key_version_id(str, Optional):
            Output only. Set by the service.

        project_id(str, Optional):
            Project Id of the new crypto key version.

        location_id(str, Optional):
            Location Id of the new crypto key version.

        key_ring_id(str, Optional):
            Keyring Id of the new crypto key version.

        crypto_key_id(str, Optional):
            Cryptokey Id of the new crypto key version.

        key_state(str, Optional):
            The current state of the `CryptoKeyVersion`_.

        algorithm(str, Optional):
            Output only. The `CryptoKeyVersionAlgorithm`_ that this `CryptoKeyVersion`_ supports.

            A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits.
            Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        import_job(str, Optional):
            Output only. The name of the `ImportJob`_ used in the most recent import of this `CryptoKeyVersion`_. Only
            present if the underlying key material was imported.

        external_protection_level_options(ExternalProtectionLevelOptions, Optional):
            ExternalProtectionLevelOptions stores a group of additional fields for configuring a CryptoKeyVersion that are specific to the EXTERNAL protection level and EXTERNAL_VPC protection levels.
            * external_key_uri(str, Optional):
                The URI for an external resource that this CryptoKeyVersion represents.

            * ekm_connection_key_path(str, Optional):
                The path to the external key material on the EKM when using EkmConnection e.g.,
                "v0/my/key". Set this field instead of external_key_uri when using an EkmConnection.

        resource_id(str, Optional): Idem resource id. Formatted as

            `projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}/cryptoKeyVersions/{crypto_key_version_id}`

        key_material(str, Optional): Base64 encoded key material. If this parameter is present will be attempted `import`_
            of the key material in the `CryptoKeyVersion`_ specified by the resource_id or in a new `CryptoKeyVersion`_
            if resource_id is missing. `import`_ requires also project_id, location_id, key_ring_id, crypto_key_id,
            algorithm and import_job parameters to be provided.

    .. _CryptoKey: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKey
    .. _CryptoKeyVersion: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion
    .. _ProtectionLevel: https://cloud.google.com/kms/docs/reference/rest/v1/ProtectionLevel
    .. _CryptoKeyVersionAlgorithm: https://cloud.google.com/kms/docs/reference/rest/v1/CryptoKeyVersionAlgorithm
    .. _protectionLevel: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion.FIELDS.protection_level
    .. _HSM: https://cloud.google.com/kms/docs/reference/rest/v1/ProtectionLevel#ENUM_VALUES.HSM
    .. _state: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion.FIELDS.state
    .. _DESTROYED: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion.CryptoKeyVersionState.ENUM_VALUES.DESTROYED
    .. _DESTROY_SCHEDULED: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion.CryptoKeyVersionState.ENUM_VALUES.DESTROY_SCHEDULED
    .. _ImportJob: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.importJobs#ImportJob
    .. _IMPORT_FAILED: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion.CryptoKeyVersionState.ENUM_VALUES.IMPORT_FAILED
    .. _ExternalProtectionLevelOptions: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion.ExternalProtectionLevelOptions
    .. _EXTERNAL: https://cloud.google.com/kms/docs/reference/rest/v1/ProtectionLevel#ENUM_VALUES.EXTERNAL
    .. _EXTERNAL_VPC: https://cloud.google.com/kms/docs/reference/rest/v1/ProtectionLevel#ENUM_VALUES.EXTERNAL_VPC
    .. _ImportCryptoKeyVersionRequest.crypto_key_version: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/import#body.request_body.FIELDS.crypto_key_version
    .. _import: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/import

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            crypto_key_test:
              gcp.cloudkms.crypto_key.present:
                - project_id: tango-gcp
                - location_id: us-east1
                - key_ring_id: idem-gcp-1
                - crypto_key_id: key-2

            crypto_key_version_test:
              gcp.cloudkms.crypto_key_version.present:
                - key_state: ENABLED
                - project_id: tango-gcp
                - location_id: us-east1
                - key_ring_id: idem-gcp-1
                - crypto_key_id: "${gcp.cloudkms.crypto_key:crypto_key_test:crypto_key_id}"

              # Update crypto key primary version with the one managed above
              gcp.cloudkms.crypto_key.present:
                - primary:
                    name: "${gcp.cloudkms.crypto_key_version:crypto_key_version_test:resource_id}"
                - project_id: tango-gcp
                - location_id: us-east1
                - key_ring_id:  idem-gcp-1
                - crypto_key_id: "${gcp.cloudkms.crypto_key:crypto_key_test:crypto_key_id}"
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
            "crypto_key_version_id": crypto_key_version_id,
        },
    ):
        result["comment"].append(
            hub.tool.gcp.comment_utils.properties_mismatch_resource_id_comment(
                RESOURCE_TYPE_FULL, name
            )
        )
    if resource_id:
        old_get_ret = await hub.exec.gcp.cloudkms.crypto_key_version.get(
            ctx, resource_id=resource_id
        )

        if not old_get_ret["result"] or (
            not old_get_ret["ret"] and get_resource_only_with_resource_id
        ):
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
            RESOURCE_TYPE_FULL,
            resource_id,
        )
        if (
            project_id
            and location_id
            and key_ring_id
            and crypto_key_id
            and crypto_key_version_id
        ):
            if (
                els.get("project_id") != project_id
                or els.get("location_id") != location_id
                or els.get("key_ring_id") != key_ring_id
                or els.get("crypto_key_id") != crypto_key_id
                or els.get("crypto_key_version_id") != str(crypto_key_version_id)
            ):
                result["result"] = False
                result["comment"].append(
                    hub.tool.gcp.comment_utils.non_updatable_properties_comment(
                        "gcp.cloudkms.crypto_key",
                        resource_id,
                        {
                            "project_id",
                            "location_id",
                            "key_ring_id",
                            "crypto_key_id",
                            "crypto_key_version_id",
                        },
                    )
                )
                return result
        else:
            project_id = els.get("project_id")
            location_id = els.get("location_id")
            key_ring_id = els.get("key_ring_id")
            crypto_key_id = els.get("crypto_key_id")
            crypto_key_version_id = els.get("crypto_key_version_id")

        result["old_state"] = old_get_ret["ret"]
    elif not get_resource_only_with_resource_id:
        if project_id and location_id and key_ring_id and crypto_key_id:
            if crypto_key_version_id:
                resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
                    RESOURCE_TYPE_FULL,
                    {
                        "project_id": project_id,
                        "location_id": location_id,
                        "key_ring_id": key_ring_id,
                        "crypto_key_id": crypto_key_id,
                        "crypto_key_version_id": crypto_key_version_id,
                    },
                )
        else:
            result["result"] = False
            result["comment"].append(
                "When creating new resource crypto_key_version_id, project_id, location_id, key_ring_id and "
                "crypto_key_id parameters are required! "
            )
            return result

        old_get_ret = await hub.exec.gcp.cloudkms.crypto_key_version.get(
            ctx, resource_id=resource_id
        )

        if not old_get_ret["result"]:
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            return result

        if old_get_ret["ret"]:
            result["old_state"] = old_get_ret["ret"]

    resource_body = {
        "state": key_state,
        "external_protection_level_options": external_protection_level_options,
    }
    resource_body = {k: v for (k, v) in resource_body.items() if v is not None}

    import_key_ret = (
        await hub.tool.gcp.cloudkms.crypto_key_version_utils.get_import_key_if_eligible(
            ctx,
            key_material is not None,
            algorithm is not None,
            import_job,
            (result.get("old_state") or {}).get("key_state")
            if "old_state" in result
            else None,
        )
    )
    if not import_key_ret["result"] and not (
        ctx.get("rerun_data") and ctx.get("rerun_data").get("imported_key_material")
    ):
        result["result"] = False
        result["comment"] += import_key_ret["comment"]
        return result

    if ctx["test"]:
        resource_id = hub.tool.gcp.resource_prop_utils.construct_resource_id(
            RESOURCE_TYPE_FULL,
            {
                "project_id": project_id,
                "location_id": location_id,
                "key_ring_id": key_ring_id,
                "crypto_key_id": crypto_key_id,
                "crypto_key_version_id": crypto_key_version_id,
            },
        )
        if import_key_ret["ret"]:
            if not result["old_state"]:
                result["comment"].append(
                    "Key material will be imported in new gcp.cloudkms.crypto_key_version"
                )
            else:
                result["comment"].append(
                    f"Key material will be re-imported in gcp.cloudkms.crypto_key_version '{resource_id}'"
                )
            return result
        if not result["old_state"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    "gcp.cloudkms.crypto_key_version", resource_id
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
                    "crypto_key_version_id": crypto_key_version_id,
                    **resource_body,
                }
            )
        else:
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                {
                    **result["old_state"],
                    **{
                        "key_state" if k == "state" else k: v
                        for k, v in resource_body.items()
                    },
                }
            )
            update_mask = hub.tool.gcp.cloudkms.patch.calc_update_mask(
                resource_body,
                {
                    "state" if k == "key_state" else k: v
                    for k, v in result["old_state"].items()
                },
            )
            if update_mask:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.would_update_comment(
                        "gcp.cloudkms.crypto_key_version", resource_id
                    )
                )
            else:
                result["comment"].append(
                    hub.tool.gcp.comment_utils.up_to_date_comment(
                        "gcp.cloudkms.crypto_key_version", resource_id
                    )
                )
        return result

    parent = hub.tool.gcp.resource_prop_utils.construct_resource_id(
        "cloudkms.projects.locations.key_rings.crypto_keys",
        {
            "project_id": project_id,
            "location_id": location_id,
            "key_ring_id": key_ring_id,
            "crypto_key_id": crypto_key_id,
        },
    )
    if import_key_ret["result"] and import_key_ret["ret"]:
        import_ret = await hub.exec.gcp.cloudkms.crypto_key_version["import"](
            ctx,
            parent=parent,
            import_job=import_job,
            import_job_pub_key=import_key_ret["ret"],
            algorithm=algorithm,
            key_material=key_material,
            crypto_key_version=resource_id,
        )
        if not import_ret["result"]:
            result["result"] = False
            result["comment"] += import_ret["comment"]
            return result

        result["new_state"] = {
            "name": name,
            "project_id": project_id,
            "location_id": location_id,
            "key_ring_id": key_ring_id,
            "crypto_key_id": crypto_key_id,
            "crypto_key_version_id": crypto_key_version_id,
            **hub.tool.gcp.cloudkms.crypto_key_version_utils.to_state(
                import_ret["ret"]
            ),
        }
        result["rerun_data"] = {"imported_key_material": True}
        result["comment"].append(
            f"Key material {'imported' if not result['old_state'] else 're-imported'} in gcp.cloudkms"
            f".crypto_key_version {result['new_state']['resource_id']} "
        )
        return result

    if result["old_state"]:
        resource_id = result["old_state"].get("resource_id", None)
        result["old_state"] = {
            "name": name,
            "project_id": project_id,
            "location_id": location_id,
            "key_ring_id": key_ring_id,
            "crypto_key_id": crypto_key_id,
            "crypto_key_version_id": crypto_key_version_id,
            **hub.tool.gcp.cloudkms.crypto_key_version_utils.to_state(
                old_get_ret["ret"]
            ),
        }
        if (
            result["old_state"].get("key_state") != "PENDING_IMPORT"
            and key_state == "PENDING_IMPORT"
            and ctx.get("rerun_data")
            and ctx.get("rerun_data").get("imported_key_material")
        ):
            key_state = result["old_state"].get("key_state")

        update_mask = hub.tool.gcp.cloudkms.patch.calc_update_mask(
            resource_body,
            {
                "state" if k == "key_state" else k: v
                for k, v in result["old_state"].items()
            },
        )
        if (
            update_mask
            and result["old_state"].get("key_state") == "DESTROY_SCHEDULED"
            and key_state == "ENABLED"
        ):
            restore_ret = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions.restore(
                ctx, name_=resource_id
            )
            if not restore_ret["result"]:
                result["result"] = False
                result["comment"] += restore_ret["comment"]
                return result
        if update_mask:
            update_ret = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions.patch(
                ctx, name_=resource_id, updateMask=update_mask, body=resource_body
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] += update_ret["comment"]
                return result

            result["comment"].append(
                hub.tool.gcp.comment_utils.update_comment(
                    "gcp.cloudkms.crypto_key_version", resource_id
                )
            )
            result["new_state"] = {
                "name": name,
                "project_id": project_id,
                "location_id": location_id,
                "key_ring_id": key_ring_id,
                "crypto_key_id": crypto_key_id,
                "crypto_key_version_id": crypto_key_version_id,
                **hub.tool.gcp.cloudkms.crypto_key_version_utils.to_state(
                    update_ret["ret"]
                ),
            }
        else:
            result["comment"].append(
                hub.tool.gcp.comment_utils.up_to_date_comment(
                    "gcp.cloudkms.crypto_key_version", resource_id
                )
            )

    else:
        create_ret = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions.create(
            ctx,
            parent=parent,
            body=resource_body,
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] += create_ret["comment"]
            return result
        result["new_state"] = {
            "name": name,
            "project_id": project_id,
            "location_id": location_id,
            "key_ring_id": key_ring_id,
            "crypto_key_id": crypto_key_id,
            "crypto_key_version_id": crypto_key_version_id,
            **hub.tool.gcp.cloudkms.crypto_key_version_utils.to_state(
                create_ret["ret"]
            ),
        }
        result["comment"].append(
            hub.tool.gcp.comment_utils.create_comment(
                "gcp.cloudkms.crypto_key_version", result["new_state"]["resource_id"]
            )
        )

    return result


async def absent(
    hub,
    ctx,
    name: str,
    crypto_key_version_id: str = None,
    project_id: str = None,
    location_id: str = None,
    key_ring_id: str = None,
    crypto_key_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Destroy crypto key version.

    After this operation the key material will no longer be stored. This version may only become `ENABLED` again if this
    version is `reimportEligible`_ and the original key material is reimported with a call to
    `KeyManagementService.ImportCryptoKeyVersion`_. Should provide either resource_id or all other *_id parameters.

    .. _KeyManagementService.ImportCryptoKeyVersion: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/import#google.cloud.kms.v1.KeyManagementService.ImportCryptoKeyVersion
    .. _reimportEligible: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion.FIELDS.reimport_eligible

    Args:
        name(str):
            Idem name.

        crypto_key_version_id(str, Optional):
            Crypto key version name used to generate resource_id if it is not provided.

        project_id(str, Optional):
            Project Id of the new crypto key version.

        location_id(str, Optional):
            Location Id of the new crypto key version .

        key_ring_id(str, Optional):
            Keyring Id of the new crypto key version.

        crypto_key_id(str, Optional):
            Cryptokey Id of the new crypto key version.

        resource_id(str, Optional):
            Idem resource id. Formatted as
            `projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{crypto_key_id}/cryptoKeyVersions/{crypto_key_version_id}`

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            {% set project_id = 'tango-gcp' %}
            {% set location_id = 'us-east1' %}
            {% set key_ring = 'key-ring' %}
            {% set crypto_key = 'crypto-key' %}
            {% set crypto_key_version = 'crypto-key-version' %}
            resource_is_absent:
              gcp.cloudkms.crypto_key_version.absent:
                - resource_id: projects/{{project_id}}/locations/{{location_id}}/keyRings/{{key_ring}}/cryptoKeys/{{crypto_key}}/cryptoKeyVersions/{{crypto_key_version}}
    """
    result = {
        "comment": [],
        "old_state": ctx.get("old_state"),
        "new_state": None,
        "name": name,
        "result": True,
    }

    get_resource_only_with_resource_id = hub.OPT.idem.get(
        "get_resource_only_with_resource_id", False
    )

    if not resource_id and not get_resource_only_with_resource_id:
        resource_id = (
            hub.tool.gcp.resource_prop_utils.construct_resource_id(
                RESOURCE_TYPE_FULL,
                {
                    "project_id": project_id,
                    "location_id": location_id,
                    "key_ring_id": key_ring_id,
                    "crypto_key_id": crypto_key_id,
                    "crypto_key_version_id": crypto_key_version_id,
                },
            )
            if project_id
            and location_id
            and key_ring_id
            and crypto_key_id
            and crypto_key_version_id
            else None
        )

    if not resource_id:
        result["comment"].append(
            hub.tool.gcp.comment_utils.already_absent_comment("gcp.compute.disk", name)
        )
        result["result"] = False
        return result

    if ctx.test:
        result["comment"].append(
            hub.tool.gcp.comment_utils.would_delete_comment(
                "gcp.cloudkms.crypto_key_version", resource_id
            )
        )
        return result

    get_ret = await hub.exec.gcp.cloudkms.crypto_key_version.get(
        ctx, resource_id=resource_id
    )
    if not get_ret["result"]:
        result["comment"] += get_ret["comment"]
        return result
    elif not get_ret["ret"] or get_ret["ret"]["state"] in [
        "DESTROYED",
        "DESTROY_SCHEDULED",
    ]:
        result["comment"].append(
            hub.tool.gcp.comment_utils.already_absent_comment(
                "gcp.cloudkms.crypto_key_version", resource_id
            )
        )
        return result

    destroy_ret = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions.destroy(
        ctx, name_=resource_id
    )

    if destroy_ret["result"]:
        result["comment"].append(
            hub.tool.gcp.comment_utils.delete_comment(
                "gcp.cloudkms.crypto_key_version", resource_id
            )
        )
    else:
        result["comment"] += destroy_ret["comment"]
        result["result"] = False

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieve the list of available crypto key versions.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.cloudkms.crypto_key_version
    """
    result = {}

    locations = await hub.exec.gcp.cloudkms.location.list(
        ctx, project=ctx.acct.project_id
    )
    if not locations["result"]:
        hub.log.warning(
            f"Could not list gcp.cloudkms.location in {ctx.acct.project_id} {locations['comment']}"
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
                    hub.log.warning(
                        f"Could not describe gcp.cloudkms.crypto_key in {key_ring['resource_id']} {key_rings['comment']}"
                    )
                else:
                    for crypto_key in crypto_keys["ret"]:
                        crypto_key_versions = (
                            await hub.exec.gcp.cloudkms.crypto_key_version.list(
                                ctx, crypto_key=crypto_key["resource_id"]
                            )
                        )
                        if not crypto_keys["result"]:
                            hub.log.warning(
                                f"Could not describe gcp.cloudkms.crypto_key in {key_ring['resource_id']} {key_rings['comment']}"
                            )
                        else:
                            for crypto_key_version in crypto_key_versions["ret"]:
                                resource_id = crypto_key_version["resource_id"]
                                result[resource_id] = {
                                    "gcp.cloudkms.crypto_key_version.present": [
                                        {parameter_key: parameter_value}
                                        if parameter_key != "state"
                                        else {"key_state": parameter_value}
                                        for parameter_key, parameter_value in crypto_key_version.items()
                                    ]
                                }
                                els = hub.tool.gcp.resource_prop_utils.get_elements_from_resource_id(
                                    RESOURCE_TYPE_FULL,
                                    resource_id,
                                )
                                p = result[resource_id][
                                    "gcp.cloudkms.crypto_key_version.present"
                                ]
                                p.append({"project_id": els["project_id"]})
                                p.append({"location_id": els["location_id"]})
                                p.append({"key_ring_id": els["key_ring_id"]})
                                p.append({"crypto_key_id": els["crypto_key_id"]})
                                p.append(
                                    {
                                        "crypto_key_version_id": els[
                                            "crypto_key_version_id"
                                        ]
                                    }
                                )

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
