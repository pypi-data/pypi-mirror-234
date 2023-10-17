"""State module for managing Images."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from idem_gcp.tool.gcp.utils import global_absent

# prevent commit hook from removing the import
absent = global_absent

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    project: str = None,
    resource_id: str = None,
    description: str = None,
    source_type: str = None,
    raw_disk: make_dataclass(
        "RawDisk",
        [
            ("container_type", str, field(default=None)),
            ("source", str, field(default=None)),
            ("sha1_checksum", str, field(default=None)),
        ],
    ) = None,
    deprecated: make_dataclass(
        "DeprecationStatus",
        [
            ("deleted", str, field(default=None)),
            ("state", str, field(default=None)),
            ("deprecated", str, field(default=None)),
            ("replacement", str, field(default=None)),
            ("obsolete", str, field(default=None)),
        ],
    ) = None,
    archive_size_bytes: str = None,
    disk_size_gb: str = None,
    source_disk: str = None,
    licenses: List[str] = None,
    image_encryption_key: make_dataclass(
        "CustomerEncryptionKey",
        [
            ("raw_key", str, field(default=None)),
            ("rsa_encrypted_key", str, field(default=None)),
            ("kms_key_name", str, field(default=None)),
            ("kms_key_service_account", str, field(default=None)),
        ],
    ) = None,
    source_disk_encryption_key: make_dataclass(
        "CustomerEncryptionKey",
        [
            ("raw_key", str, field(default=None)),
            ("rsa_encrypted_key", str, field(default=None)),
            ("kms_key_name", str, field(default=None)),
            ("kms_key_service_account", str, field(default=None)),
        ],
    ) = None,
    labels: Dict[str, str] = None,
    label_fingerprint: str = None,
    guest_os_features: List[
        make_dataclass("GuestOsFeature", [("type", str, field(default=None))])
    ] = None,
    license_codes: List[str] = None,
    source_image: str = None,
    source_image_encryption_key: make_dataclass(
        "CustomerEncryptionKey",
        [
            ("raw_key", str, field(default=None)),
            ("rsa_encrypted_key", str, field(default=None)),
            ("kms_key_name", str, field(default=None)),
            ("kms_key_service_account", str, field(default=None)),
        ],
    ) = None,
    source_snapshot: str = None,
    source_snapshot_encryption_key: make_dataclass(
        "CustomerEncryptionKey",
        [
            ("raw_key", str, field(default=None)),
            ("rsa_encrypted_key", str, field(default=None)),
            ("kms_key_name", str, field(default=None)),
            ("kms_key_service_account", str, field(default=None)),
        ],
    ) = None,
    storage_locations: List[str] = None,
    shielded_instance_initial_state: make_dataclass(
        "InitialStateConfig",
        [
            (
                "keks",
                List[
                    make_dataclass(
                        "FileContentBuffer",
                        [
                            ("content", str, field(default=None)),
                            ("file_type", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            (
                "pk",
                make_dataclass(
                    "FileContentBuffer",
                    [
                        ("content", str, field(default=None)),
                        ("file_type", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "dbs",
                List[
                    make_dataclass(
                        "FileContentBuffer",
                        [
                            ("content", str, field(default=None)),
                            ("file_type", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            (
                "dbxs",
                List[
                    make_dataclass(
                        "FileContentBuffer",
                        [
                            ("content", str, field(default=None)),
                            ("file_type", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
        ],
    ) = None,
    architecture: str = None,
) -> Dict[str, Any]:
    r"""Creates an image in the specified project using the data included in the request.

    Args:
        name(str, Optional):
            An Idem name of the resource.

        project(str, Optional):
            Project ID for this request. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        description(str, Optional):
            An optional description of this resource. Defaults to None.

        source_type(str, Optional):
            The type of the image used to create this disk. The default and only valid value is RAW.

        raw_disk(Dict[str, Any], Optional):
            The parameters of the raw disk image.

            * container_type(str, Optional):
                The format used to encode and transmit the block device, which should be TAR.
                This is just a container and transmission format and not a runtime format.
                Provided by the client when the disk image is created.
            * source(str, Optional):
                The full Google Cloud Storage URL where the raw disk image archive is stored.
                The following are valid formats for the URL:

                - https://storage.googleapis.com/bucket_name/image_archive_name
                - https://storage.googleapis.com/bucket_name/folder_name/ image_archive_name

                In order to create an image, you must provide the full or partial URL of one of the following:

                - The rawDisk.source URL
                - The sourceDisk URL
                - The sourceImage URL
                - The sourceSnapshot URL
            * sha1_checksum(str, Optional):
                [Deprecated] This field is deprecated.
                An optional SHA1 checksum of the disk image before unpackaging provided by the client
                when the disk image is created.

        deprecated(Dict[str, Any], Optional):
            Deprecation status for a public resource.

            * deleted(str, Optional):
                An optional RFC3339 timestamp on or after which the state of this resource
                is intended to change to DELETED. This is only informational and the status
                will not change unless the client explicitly changes it.
            * state(str, Optional):
                The deprecation state of this resource. This can be ACTIVE, DEPRECATED, OBSOLETE, or DELETED.
                Operations which communicate the end of life date for an image, can use ACTIVE.
                Operations which create a new resource using a DEPRECATED resource will return successfully,
                but with a warning indicating the deprecated resource and recommending its replacement.
                Operations which use OBSOLETE or DELETED resources will be rejected and result in an error.
            * deprecated(str, Optional):
                An optional RFC3339 timestamp on or after which the state of this resource
                is intended to change to DEPRECATED. This is only informational and the status
                will not change unless the client explicitly changes it.
            * replacement(str, Optional):
                The URL of the suggested replacement for a deprecated resource.
                The suggested replacement resource must be the same kind of resource as the deprecated resource.
            * obsolete(str, Optional):
                An optional RFC3339 timestamp on or after which the state of this resource
                is intended to change to OBSOLETE. This is only informational and the status
                will not change unless the client explicitly changes it.

        archive_size_bytes(str, Optional):
            Size of the image tar.gz archive stored in Google Cloud Storage (in bytes).

        disk_size_gb(str, Optional):
            Size of the image when restored onto a persistent disk (in GB).

        source_disk(str, Optional):
            URL of the source disk used to create this image.
            For example, the following are valid values:

            - https://www.googleapis.com/compute/v1/projects/project/zones/zone/disks/disk
            - projects/project/zones/zone/disks/disk
            - zones/zone/disks/disk

            In order to create an image, you must provide the full or partial URL of one of the following:

            - The rawDisk.source URL
            - The sourceDisk URL
            - The sourceImage URL
            - The sourceSnapshot URL

        licenses(List[str], Optional):
            Any applicable license URI.

        image_encryption_key(Dict[str, Any], Optional):
            Encrypts the image using a customer-supplied encryption key. After you encrypt an image with a
            customer-supplied key, you must provide the same key if you use the image later
            (e.g. to create a disk from the image). Customer-supplied encryption keys do not protect access to metadata
            of the disk. If you do not provide an encryption key when creating the image, then the disk will be
            encrypted using an automatically generated key and you do not need to provide a key to use the image later.

            * raw_key(str, Optional):
                    Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt
                    or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey.
                    For example:

                    \"raw_key\": \"SGVsbG8gZnJvbSBHb29nbGUgQ2xvdWQgUGxhdGZvcm0=\"

            * rsa_encrypted_key(str, Optional):
                Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to
                either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey.
                For example:

                \"rsa_encrypted_key\":
                \"ieCx/NcW06PcT7Ep1X6LUTc/hLvUDYyzSZPPVCVPTVEohpeHASqC8uw5TzyO9U+Fka9JFH z0mBibXUInrC/jEk014kCK/
                NPjYgEMOyssZ4ZINPKxlUh2zn1bV+MCaTICrdmuSBTWlUUiFoD D6PYznLwh8ZNdaheCeZ8ewEXgFQ8V+sDroLaN3Xs3MDTXQEM
                MoNUXMCZEIpg9Vtp9x2oe==\"

                The key must meet the following requirements before you can provide it to Compute Engine:

                1. The key is wrapped using a RSA public key certificate provided by Google.
                2. After being wrapped, the key must be encoded in RFC 4648 base64 encoding.

                Gets the RSA public key certificate provided by Google at:
                https://cloud-certs.storage.googleapis.com/google-cloud-csek-ingress.pem

            * kms_key_name(str, Optional):
                The name of the encryption key that is stored in Google Cloud KMS.
                For example:

                \"kms_key_name\":
                \"projects/kms_project_id/locations/region/keyRings/ key_region/cryptoKeys/key

            * kms_key_service_account(str, Optional):
                The service account being used for the encryption request for the given KMS key. If absent,
                the Compute Engine default service account is used. For example:

                \"kms_key_service_account\":
                \"name@project_id.iam.gserviceaccount.com/

        source_disk_encryption_key(Dict[str, Any], Optional):
            The customer-supplied encryption key of the source disk.
            Required if the source disk is protected by a customer-supplied encryption key."

            * raw_key(str, Optional):
                Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rawKey": "SGVsbG8gZnJvbSBHb29nbGUgQ2xvdWQgUGxhdGZvcm0="
            * rsa_encrypted_key(str, Optional):
                Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rsaEncryptedKey": "ieCx/NcW06PcT7Ep1X6LUTc/hLvUDYyzSZPPVCVPTVEohpeHASqC8uw5TzyO9U+Fka9JFH z0mBibXUInrC/jEk014kCK/NPjYgEMOyssZ4ZINPKxlUh2zn1bV+MCaTICrdmuSBTWlUUiFoD D6PYznLwh8ZNdaheCeZ8ewEXgFQ8V+sDroLaN3Xs3MDTXQEMMoNUXMCZEIpg9Vtp9x2oe==" The key must meet the following requirements before you can provide it to Compute Engine: 1. The key is wrapped using a RSA public key certificate provided by Google. 2. After being wrapped, the key must be encoded in RFC 4648 base64 encoding. Gets the RSA public key certificate provided by Google at: https://cloud-certs.storage.googleapis.com/google-cloud-csek-ingress.pem
            * kms_key_name(str, Optional):
                The name of the encryption key that is stored in Google Cloud KMS. For example: "kmsKeyName": "projects/kms_project_id/locations/region/keyRings/ key_region/cryptoKeys/key
            * kms_key_service_account(str, Optional):
                The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. For example: "kmsKeyServiceAccount": "name@project_id.iam.gserviceaccount.com/

        labels(Dict[str, str], Optional):
            Labels to apply to this image. These can be later modified by the setLabels method.

        label_fingerprint(str, Optional):
            A fingerprint for the labels being applied to this image, which is essentially a hash of the labels
            used for optimistic locking. The fingerprint is initially generated by Compute Engine and changes after
            every request to modify or update labels. You must always provide an up-to-date fingerprint hash
            in order to update or change labels, otherwise the request will fail with error 412 conditionNotMet.
            To see the latest fingerprint, make a get() request to retrieve an image.

        guest_os_features(List[Dict[str, Any]], Optional):
            A list of features to enable on the guest operating system. Applicable only for bootable images.
            To see a list of available options, see the guestOSfeatures[].type parameter.

            * type(str, Optional):
                The ID of a supported feature. To add multiple values,
                use commas to separate values. Set to one or more of the following values:

                - VIRTIO_SCSI_MULTIQUEUE
                - WINDOWS
                - MULTI_IP_SUBNET
                - UEFI_COMPATIBLE
                - GVNIC
                - SEV_CAPABLE
                - SUSPEND_RESUME_COMPATIBLE
                - SEV_SNP_CAPABLE

                For more information, see Enabling guest operating system features.

        license_codes(List[str], Optional):
            Integer license codes indicating which licenses are attached to this image.

        source_image(str, Optional):
            URL of the source image used to create this image. The following are valid formats for the URL:

            - https://www.googleapis.com/compute/v1/projects/project_id/global/images/image_name
            - projects/project_id/global/images/image_name

            In order to create an image, you must provide the full or partial URL of one of the following:

            - The rawDisk.source URL
            - The sourceDisk URL
            - The sourceImage URL
            - The sourceSnapshot URL

        source_image_encryption_key(Dict[str, Any], Optional):
            The customer-supplied encryption key of the source image.
            Required if the source image is protected by a customer-supplied encryption key.

            * raw_key(str, Optional):
                Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rawKey": "SGVsbG8gZnJvbSBHb29nbGUgQ2xvdWQgUGxhdGZvcm0="
            * rsa_encrypted_key(str, Optional):
                Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rsaEncryptedKey": "ieCx/NcW06PcT7Ep1X6LUTc/hLvUDYyzSZPPVCVPTVEohpeHASqC8uw5TzyO9U+Fka9JFH z0mBibXUInrC/jEk014kCK/NPjYgEMOyssZ4ZINPKxlUh2zn1bV+MCaTICrdmuSBTWlUUiFoD D6PYznLwh8ZNdaheCeZ8ewEXgFQ8V+sDroLaN3Xs3MDTXQEMMoNUXMCZEIpg9Vtp9x2oe==" The key must meet the following requirements before you can provide it to Compute Engine: 1. The key is wrapped using a RSA public key certificate provided by Google. 2. After being wrapped, the key must be encoded in RFC 4648 base64 encoding. Gets the RSA public key certificate provided by Google at: https://cloud-certs.storage.googleapis.com/google-cloud-csek-ingress.pem
            * kms_key_name(str, Optional):
                The name of the encryption key that is stored in Google Cloud KMS. For example: "kmsKeyName": "projects/kms_project_id/locations/region/keyRings/ key_region/cryptoKeys/key
            * kms_key_service_account(str, Optional):
                The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. For example: "kmsKeyServiceAccount": "name@project_id.iam.gserviceaccount.com/

        source_snapshot(str, Optional):
            URL of the source snapshot used to create this image. The following are valid formats for the URL:

            - https://www.googleapis.com/compute/v1/projects/project_id/global/snapshots/snapshot_name
            - projects/project_id/global/snapshots/snapshot_name

            In order to create an image, you must provide the full or partial URL of one of the following:

            - The rawDisk.source URL
            - The sourceDisk URL
            - The sourceImage URL
            - The sourceSnapshot URL

        source_snapshot_encryption_key(Dict[str, Any], Optional):
            The customer-supplied encryption key of the source snapshot.
            Required if the source snapshot is protected by a customer-supplied encryption key.

            * raw_key(str, Optional):
                Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rawKey": "SGVsbG8gZnJvbSBHb29nbGUgQ2xvdWQgUGxhdGZvcm0="
            * rsa_encrypted_key(str, Optional):
                Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rsaEncryptedKey": "ieCx/NcW06PcT7Ep1X6LUTc/hLvUDYyzSZPPVCVPTVEohpeHASqC8uw5TzyO9U+Fka9JFH z0mBibXUInrC/jEk014kCK/NPjYgEMOyssZ4ZINPKxlUh2zn1bV+MCaTICrdmuSBTWlUUiFoD D6PYznLwh8ZNdaheCeZ8ewEXgFQ8V+sDroLaN3Xs3MDTXQEMMoNUXMCZEIpg9Vtp9x2oe==" The key must meet the following requirements before you can provide it to Compute Engine: 1. The key is wrapped using a RSA public key certificate provided by Google. 2. After being wrapped, the key must be encoded in RFC 4648 base64 encoding. Gets the RSA public key certificate provided by Google at: https://cloud-certs.storage.googleapis.com/google-cloud-csek-ingress.pem
            * kms_key_name(str, Optional):
                The name of the encryption key that is stored in Google Cloud KMS. For example: "kmsKeyName": "projects/kms_project_id/locations/region/keyRings/ key_region/cryptoKeys/key
            * kms_key_service_account(str, Optional):
                The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. For example: "kmsKeyServiceAccount": "name@project_id.iam.gserviceaccount.com/

        storage_locations(List[str], Optional):
            Cloud Storage bucket storage location of the image (regional or multi-regional).

        shielded_instance_initial_state(Dict[str, Any], Optional):
            Set the secure boot keys of shielded instance.

            * keks(List[Dict[str, Any]], Optional):
                The Key Exchange Key (KEK).

                * file_type(str, Optional):
                    The file type of source file.
                    Enum type. Allowed values:
                        "BIN"
                        "UNDEFINED"
                        "X509"
                * content(str, Optional):
                    The raw content in the secure keys file.
            * dbs(List[Dict[str, Any]], Optional):
                The Key Database (db).

                * file_type (str, Optional):
                    The file type of source file.
                    Enum type. Allowed values:
                        "BIN"
                        "UNDEFINED"
                        "X509"
                * content (str, Optional):
                    The raw content in the secure keys file.

            * dbxs (List[Dict[str, Any]], Optional):
                The forbidden key database (dbx).

                * file_type (str, Optional):
                    The file type of source file.
                    Enum type. Allowed values:
                        "BIN"
                        "UNDEFINED"
                        "X509"
                * content (str, Optional):
                    The raw content in the secure keys file.
            * pk (Dict[str, Any], Optional):
                The Platform Key (PK).

                * file_type (str, Optional):
                    The file type of source file.
                    Enum type. Allowed values:
                        "BIN"
                        "UNDEFINED"
                        "X509"
                * content (str, Optional):
                    The raw content in the secure keys file.

        architecture(str, Optional):
            The architecture of the image. Valid values are ARM64 or X86_64.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            example_resource_name:
              gcp.compute.image.present:
                - name: value
                - project: value
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    # TODO uncomment below line, when implementation is added
    # project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    result["comment"].append(
        "No-op: There is no create/update function for gcp.compute.image"
    )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves a list of images.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.image
    """
    result = {}

    describe_ret = await hub.exec.gcp.compute.image.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(f"Could not describe images {describe_ret['comment']}")
        return {}

    for resource in describe_ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "gcp.compute.image.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
