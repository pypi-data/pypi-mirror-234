"""State module for managing Machine Images."""
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
    source_instance: str = None,
    storage_locations: List[str] = None,
    source_disk_encryption_keys: List[
        make_dataclass(
            "SourceDiskEncryptionKey",
            [
                ("source_disk", str, field(default=None)),
                (
                    "disk_encryption_key",
                    make_dataclass(
                        "CustomerEncryptionKey",
                        [
                            ("kms_key_service_account", str, field(default=None)),
                            ("rsa_encrypted_key", str, field(default=None)),
                            ("kms_key_name", str, field(default=None)),
                            ("raw_key", str, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
            ],
        )
    ] = None,
    description: str = None,
    saved_disks: List[
        make_dataclass(
            "SavedDisk",
            [
                ("kind", str, field(default="compute#savedDisk")),
                ("storage_bytes_status", str, field(default=None)),
                ("architecture", str, field(default=None)),
                ("storage_bytes", str, field(default=None)),
                ("source_disk", str, field(default=None)),
            ],
        )
    ] = None,
    guest_flush: bool = None,
    machine_image_encryption_key: make_dataclass(
        "CustomerEncryptionKey",
        [
            ("kms_key_service_account", str, field(default=None)),
            ("rsa_encrypted_key", str, field(default=None)),
            ("raw_key", str, field(default=None)),
            ("kms_key_name", str, field(default=None)),
        ],
    ) = None,
) -> Dict[str, Any]:
    r"""Creates a machine image in the specified project using the data that is included in the request. If you are creating a new machine image to update an existing instance, your new machine image should use the same network or, if applicable, the same subnetwork as the original instance.

    Args:
        name(str):
            An Idem name of the resource.

        project(str, Optional):
            Project ID for this request.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        source_instance(str, Optional):
            The source instance used to create the machine image. You can provide this as a partial or full URL to the resource. For example, the following are valid values:

            - https://www.googleapis.com/compute/v1/projects/project/zones/zone/instances/instance
            - projects/project/zones/zone/instances/instance

            Defaults to None.

        storage_locations(list[str], Optional):
            The regional or multi-regional Cloud Storage bucket location where the machine image is stored. Defaults to None.

        source_disk_encryption_keys(list[Dict[str, Any]], Optional):
            [Input Only] The customer-supplied encryption key of the disks attached to the source instance. Required if the source disk is protected by a customer-supplied encryption key. Defaults to None.

            * source_disk(str, Optional):
                URL of the disk attached to the source instance. This can be a full or valid partial URL. For example, the following are valid values:

                - https://www.googleapis.com/compute/v1/projects/project/zones/zone/disks/disk
                - projects/project/zones/zone/disks/disk
                - zones/zone/disks/disk

            * disk_encryption_key(Dict[str, Any], Optional):
                The customer-supplied encryption key of the source disk. Required if the source disk is protected by a customer-supplied encryption key.

                * kms_key_service_account(str, Optional):
                    The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. For example: "kmsKeyServiceAccount": "name@project_id.iam.gserviceaccount.com/"
                * rsa_encrypted_key(str, Optional):
                    Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rsaEncryptedKey": "ieCx/NcW06PcT7Ep1X6LUTc/hLvUDYyzSZPPVCVPTVEohpeHASqC8uw5TzyO9U+Fka9JFH z0mBibXUInrC/jEk014kCK/NPjYgEMOyssZ4ZINPKxlUh2zn1bV+MCaTICrdmuSBTWlUUiFoD D6PYznLwh8ZNdaheCeZ8ewEXgFQ8V+sDroLaN3Xs3MDTXQEMMoNUXMCZEIpg9Vtp9x2oe==" The key must meet the following requirements before you can provide it to Compute Engine: 1. The key is wrapped using a RSA public key certificate provided by Google. 2. After being wrapped, the key must be encoded in RFC 4648 base64 encoding. Gets the RSA public key certificate provided by Google at: https://cloud-certs.storage.googleapis.com/google-cloud-csek-ingress.pem
                * kms_key_name(str, Optional):
                    The name of the encryption key that is stored in Google Cloud KMS. For example: "kmsKeyName": "projects/kms_project_id/locations/region/keyRings/ key_region/cryptoKeys/key
                * raw_key(str, Optional):
                    Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rawKey": "SGVsbG8gZnJvbSBHb29nbGUgQ2xvdWQgUGxhdGZvcm0="

        description(str, Optional):
            An optional description of this resource. Provide this property when you create the resource. Defaults to None.

        saved_disks(list[Dict[str, Any]], Optional):
            An array of Machine Image specific properties for disks attached to the source instance. Defaults to None.

            * kind(str, Optional):
                [Output Only] Type of the resource. Always compute#savedDisk for attached disks.
            * storage_bytes_status (str, Optional):
                [Output Only] An indicator whether storageBytes is in a stable state or it is being adjusted as a result of shared storage reallocation. This status can either be UPDATING, meaning the size of the snapshot is being updated, or UP_TO_DATE, meaning the size of the snapshot is up-to-date.
            * architecture(str, Optional):
                [Output Only] The architecture of the attached disk.
            * storage_bytes(str, Optional):
                [Output Only] Size of the individual disk snapshot used by this machine image.
            * source_disk(str, Optional):
                Specifies a URL of the disk attached to the source instance.

        guest_flush(bool, Optional):
            [Input Only] Whether to attempt an application consistent machine image by informing the OS to prepare for the snapshot process. Defaults to None.

        machine_image_encryption_key(Dict[str, Any], Optional):
            Encrypts the machine image using a customer-supplied encryption key. After you encrypt a machine image using a customer-supplied key, you must provide the same key if you use the machine image later. For example, you must provide the encryption key when you create an instance from the encrypted machine image in a future request. Customer-supplied encryption keys do not protect access to metadata of the machine image. If you do not provide an encryption key when creating the machine image, then the machine image will be encrypted using an automatically generated key and you do not need to provide a key to use the machine image later. Defaults to None.

            * kms_key_service_account(str, Optional):
                The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. For example: "kmsKeyServiceAccount": "name@project_id.iam.gserviceaccount.com/"
            * rsa_encrypted_key(str, Optional):
                Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rsaEncryptedKey": "ieCx/NcW06PcT7Ep1X6LUTc/hLvUDYyzSZPPVCVPTVEohpeHASqC8uw5TzyO9U+Fka9JFH z0mBibXUInrC/jEk014kCK/NPjYgEMOyssZ4ZINPKxlUh2zn1bV+MCaTICrdmuSBTWlUUiFoD D6PYznLwh8ZNdaheCeZ8ewEXgFQ8V+sDroLaN3Xs3MDTXQEMMoNUXMCZEIpg9Vtp9x2oe==" The key must meet the following requirements before you can provide it to Compute Engine: 1. The key is wrapped using a RSA public key certificate provided by Google. 2. After being wrapped, the key must be encoded in RFC 4648 base64 encoding. Gets the RSA public key certificate provided by Google at: https://cloud-certs.storage.googleapis.com/google-cloud-csek-ingress.pem
            * kms_key_name(str, Optional):
                The name of the encryption key that is stored in Google Cloud KMS. For example: "kmsKeyName": "projects/kms_project_id/locations/region/keyRings/ key_region/cryptoKeys/key
            * raw_key(str, Optional):
                Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rawKey": "SGVsbG8gZnJvbSBHb29nbGUgQ2xvdWQgUGxhdGZvcm0="

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            example_resource_name:
              gcp.compute.machine_image.present:
                - project: project-name
                - source_instance: https://www.googleapis.com/compute/v1/projects/project-name/zones/zone-name/instances/instance-name
    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    if ctx.get("wrapper_result"):
        result = ctx.get("wrapper_result")

    request_body = {
        "storage_locations": storage_locations,
        "guest_flush": guest_flush,
        "source_instance": source_instance,
        "description": description,
        "name": name,
        "saved_disks": saved_disks,
        "machine_image_encryption_key": machine_image_encryption_key,
        "source_disk_encryption_keys": source_disk_encryption_keys,
    }

    operation = None
    plan_state = {"resource_id": resource_id, **request_body}
    plan_state = {k: v for (k, v) in plan_state.items() if v is not None}

    if result["old_state"]:
        resource_id = result["old_state"].get("resource_id", None)

        changes = hub.tool.gcp.utils.compare_states(
            result["old_state"], plan_state, "compute.machine_image"
        )

        if not changes:
            result["result"] = True
            result["comment"].append(
                hub.tool.gcp.comment_utils.up_to_date_comment(
                    "gcp.compute.machine_image", name
                )
            )
            result["new_state"] = result["old_state"]
            return result

        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_update_comment(
                    "gcp.compute.machine_image", name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                plan_state
            )
            return result
        else:
            result["comment"].append(
                hub.tool.gcp.comment_utils.no_resource_update_comment(
                    "gcp.compute.machine_image"
                )
            )
            return result
    else:
        # Create machine image
        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    "gcp.compute.machine_image", name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                plan_state
            )
            result["new_state"][
                "resource_id"
            ] = hub.tool.gcp.resource_prop_utils.construct_resource_id(
                "compute.machine_image", {**locals(), "machineImage": name}
            )
            return result

        create_ret = await hub.exec.gcp_api.client.compute.machine_image.insert(
            ctx, project=project, body=request_body
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] += create_ret["comment"]
            return result

        if hub.tool.gcp.operation_utils.is_operation(create_ret["ret"]):
            operation = create_ret["ret"]

    if operation:
        operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            operation.get("selfLink"), "compute.global_operation"
        )

        result["rerun_data"] = {
            "operation_id": operation_id,
            "old_state": result["old_state"],
        }
        return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves a list of machine images that are contained within the specified project.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.machine_image
    """
    result = {}

    describe_ret = await hub.exec.gcp_api.client.compute.machine_image.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(
            f"Could not describe gcp.compute.machine_image {describe_ret['comment']}"
        )
        return {}

    for resource in describe_ret["ret"].get("items", []):
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "gcp.compute.machine_image.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
