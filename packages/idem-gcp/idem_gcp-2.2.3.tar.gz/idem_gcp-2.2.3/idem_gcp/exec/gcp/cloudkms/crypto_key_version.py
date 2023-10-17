"""Exec module for managing Cloud Key Management Service crypto key versions."""
import base64
from typing import Any
from typing import Dict


__func_alias__ = {"list_": "list", "import_": "import"}


async def get(
    hub,
    ctx,
    resource_id: str,
):
    """Returns a crypto key version by its Idem resource ID.

    Args:
        resource_id(str):
            Idem resource ID. ``projects/{project id}/locations/{location id}/keyRings/{keyRing}/cryptoKeys/{cryptoKey}/cryptoKeyVersions/{cryptoKeyVersion}``

    Returns:
        CryptoKeyVersion resource

    Examples:
        .. code-block:: sls

            {% set project_id = 'project-name' %}
            {% set location_id = 'us-east1' %}
            {% set key_ring = 'key-ring' %}
            {% set crypto_key = 'crypto-key' %}
            {% set crypto_key_version = 'crypto-key-version' %}
            get-crypto-key-version:
                exec.run:
                    - path: gcp.cloudkms.crypto_key_version.get
                    - kwargs:
                        resource_id: projects/{{project_id}}/locations/{{location_id}}/keyRings/{{key_ring}}/cryptoKeys/{{crypto_key}}/cryptoKeyVersions/{{crypto_key_version}}
    """
    result = {
        "comment": [],
        "ret": [],
        "result": True,
    }

    crypto_key = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions.get(
        ctx, _name=resource_id
    )

    if not crypto_key["result"]:
        result["comment"] += crypto_key["comment"]
        result["result"] = False
        return result

    result["ret"] = crypto_key["ret"]

    if not result["ret"]:
        result["comment"] += (
            hub.tool.gcp.comment_utils.get_empty_comment(
                "gcp.cloudkms.crypto_key_version", resource_id
            ),
        )

    return result


async def list_(
    hub,
    ctx,
    crypto_key: str,
    filter_: (str, "alias=filter") = None,
    order_by: str = None,
) -> Dict[str, Any]:
    r"""Retrieves the crypto key versions in a crypto key.

    Args:
        crypto_key(str):
            crypto key resource_id.

        filter(str, Optional):
            Only include resources that match the filter in the response. For more information, see
            `Sorting and filtering list results`_.

        order_by(str, Optional):
            Specify how the results should be sorted. If not specified, the results will be sorted in the default order.
            For more information, see `Sorting and filtering list results`_.

    .. _Sorting and filtering list results: https://cloud.google.com/kms/docs/sorting-and-filtering

    Examples:
        .. code-block:: sls

            list-crypto-key_versions-filtered:
                exec.run:
                   - path: gcp.cloudkms.crypto_key_version.list
                   - kwargs:
                         crypto_key: projects/project-name/locations/global/keyRings/kr-global-test
                         filter_: algorithm = GOOGLE_SYMMETRIC_ENCRYPTION
    """
    result = {
        "comment": [],
        "ret": [],
        "result": True,
    }

    crypto_key_versions = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions.list(
        ctx, parent=crypto_key, filter=filter_, orderBy=order_by
    )
    if not crypto_key_versions["result"]:
        result["comment"] += crypto_key_versions["comment"]
        result["result"] = False
        return result

    result["ret"] = crypto_key_versions["ret"].get("items", [])

    return result


async def import_(
    hub,
    ctx,
    parent: str,
    import_job: str,
    import_job_pub_key: str,
    algorithm: str,
    key_material: str,
    crypto_key_version: str = None,
) -> Dict[str, Any]:
    r"""Import key material in crypto key version.

    Args:
        parent(str):
            Required. The Idem resource_id of the `CryptoKey`_ to be imported into.
            The create permission is only required on this key when creating a new `CryptoKeyVersion`_.
            Authorization requires the following `IAM`_ permission on the specified resource parent:

            - cloudkms.cryptoKeyVersions.create
        import_job(str):
            Required. Idem resource_id of the import job to be used.
        import_job_pub_key(str):
            Required. PEM encoded public key of the import job to be used to wrap this key material.
            Authorization requires the following `IAM`_ permission on the specified resource import_job:

            - cloudkms.importjobs.useToImport
        algorithm(str):
            Required. The `algorithm`_ of the key being imported. This does not need to match the `versionTemplate`_ of the
            `CryptoKey`_ this version imports into.
        key_material(str):
            Base64 encoded key material. If importing symmetric key material, it is expected that the key contains
            plain bytes. If importing asymmetric key material, it is expected that the key is in
            PKCS#8-encoded DER format (the PrivateKeyInfo structure from RFC 5208).
        crypto_key_version(str, Optional):
            The optional Idem resource_id of an existing `CryptoKeyVersion`_ to target for an import operation. If this field is
            not present, a new `CryptoKeyVersion`_ containing the supplied key material is created.
            If this field is present, the supplied key material is imported into the existing `CryptoKeyVersion`_. To
            import into an existing `CryptoKeyVersion`_, the `CryptoKeyVersion`_ must be a child of
            `ImportCryptoKeyVersionRequest.parent`_, have been previously created via [cryptoKeyVersions.import][], and
            be in `DESTROYED`_ or `IMPORT_FAILED`_ state. The key material and algorithm must match the previous
            `CryptoKeyVersion`_ exactly if the `CryptoKeyVersion`_ has ever contained key material.
            Authorization requires the following `IAM`_ permission on the specified resource cryptoKeyVersion:

            - cloudkms.cryptoKeyVersions.update

    .. _CryptoKeyVersion: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion
    .. _name: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion.FIELDS.name
    .. _ImportCryptoKeyVersionRequest.parent: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/import#body.PATH_PARAMETERS.parent
    .. _DESTROYED: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion.CryptoKeyVersionState.ENUM_VALUES.DESTROYED
    .. _IMPORT_FAILED: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions#CryptoKeyVersion.CryptoKeyVersionState.ENUM_VALUES.IMPORT_FAILED
    .. _IAM: https://cloud.google.com/iam/docs/
    .. _CryptoKey: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKey
    .. _algorithm: https://cloud.google.com/kms/docs/reference/rest/v1/CryptoKeyVersionAlgorithm
    .. _versionTemplate: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys#CryptoKey.FIELDS.version_template
    .. _ImportJob: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.importJobs#ImportJob
    .. _RSA_OAEP_3072_SHA1_AES_256: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.importJobs#ImportMethod.ENUM_VALUES.RSA_OAEP_3072_SHA1_AES_256
    .. _RSA_OAEP_4096_SHA1_AES_256: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.importJobs#ImportMethod.ENUM_VALUES.RSA_OAEP_4096_SHA1_AES_256
    .. _public_key: https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.importJobs#ImportJob.FIELDS.public_key

    Returns:
        Dict[str, Any] - If successful, the response body contains an instance of `CryptoKeyVersion`_.

    Examples:
        .. code-block:: sls

            {% set project_id = 'project-name' %}
            {% set location_id = 'us-east1' %}
            {% set key_ring_id = 'key-ring' %}
            {% set crypto_key_id = 'crypto-key' %}
            {% set import_job_id = 'import-job-id' %}

            import-job:
              gcp.cloudkms.import_job.present:
                  - import_method: RSA_OAEP_3072_SHA1_AES_256
                  - protection_level: SOFTWARE
                  - project_id: {{project_id}}
                  - location_id: {{location_id}}
                  - key_ring_id: {{key_ring_id}}
                  - import_job_id: {{import_job_id}}

            import-crypto-key:
                exec.run:
                   - path: gcp.cloudkms.crypto_key_version.import
                   - kwargs:
                         parent: projects/{{project_id}}/locations/{{location_id}}/keyRings/{{key_ring_id}}/cryptoKeys/{{crypto_key_id}}
                         import_job: ${gcp.cloudkms.import_job:import-job:resource_id}
                         import_job_pub_key: ${gcp.cloudkms.import_job:import-job:public_key:pem}
                         algorithm: "EC_SIGN_P256_SHA256"
                         key_material: rr5Y2UNi6+i3UQDrR8PO6s5ajAorN/SnHfZu+OCHx+w=
    """
    result = {
        "comment": [],
        "ret": [],
        "result": True,
    }

    rsa_aes_wrapped_key = hub.tool.gcp.cloudkms.crypto_key_version_utils.wrap_key(
        base64.b64decode(key_material), import_job_pub_key
    )

    import_ret = await hub.exec.gcp_api.client.cloudkms.projects.locations.key_rings.crypto_keys.crypto_key_versions.import_(
        ctx,
        parent=parent,
        body={
            "algorithm": algorithm,
            "importJob": import_job,
            "rsaAesWrappedKey": base64.urlsafe_b64encode(rsa_aes_wrapped_key).decode(
                "UTF-8"
            ),
            "cryptoKeyVersion": crypto_key_version,
        },
    )

    result["result"] = import_ret["result"]
    result["comment"] += import_ret["comment"]
    result["ret"] = import_ret["ret"]
    return result
