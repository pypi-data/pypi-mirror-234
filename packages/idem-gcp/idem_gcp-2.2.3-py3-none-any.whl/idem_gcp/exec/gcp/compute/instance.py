"""Exec module for managing Instances."""

__func_alias__ = {"list_": "list"}

from dataclasses import make_dataclass, field
from typing import Any, Dict, List

from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext
from idem_gcp.tool.gcp.generate.exec_param import ExecParam
from idem_gcp.tool.gcp.generate.scope import Scope


async def list_(
    hub,
    ctx,
    project: str = None,
    zone: str = None,
    filter_: (str, "alias=filter") = None,
    order_by: str = None,
):
    r"""Retrieves the list of instances contained within the specified zone.

    Args:
        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            Name of the zone for this request.

        filter(str, Optional):
            A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = \"Intel Skylake\") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = \"Intel Skylake\") OR (cpuPlatform = \"Intel Broadwell\") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq \"double quoted literal\"` `(fieldname1 eq literal) (fieldname2 ne \"literal\")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name "instance", you would use `name ne .*instance`.

        order_by(str, Optional):
            Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy=\"creationTimestamp desc\"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance.list
              - kwargs:
                  project: project-name
                  zone: zone-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    # GCP method name is simply the name of this func or the one from __func_alias - we can pass it
    # also we can pass the resource name based on the file name
    execution_context = ExecutionContext(
        resource_type="compute.instance",
        method_name="list",
        method_params={
            "ctx": ctx,
            "project": project,
            "zone": zone,
            "filter": filter_,
            "order_by": order_by,
        },
        exec_params={
            ExecParam.SCOPED_FUNCTIONS: {
                Scope.ZONAL: "list",
                Scope.GLOBAL: "aggregatedList",
            }
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def get(
    hub,
    ctx,
    resource_id: str = None,
    project: str = None,
    zone: str = None,
    name: str = None,
):
    r"""Returns the specified Instance resource. Gets a list of available instances by making a list() request.

    Args:
        resource_id(str, Optional):
            An identifier of the resource in the provider.

        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            Name of the zone for this request.

        name(str, Optional):
            Name of the instance resource to return.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance.get
              - kwargs:
                  project: project-name
                  zone: zone-name
                  name: instance-name
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type="compute.instance",
        method_name="get",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "zone": zone,
            "instance": name,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def set_disk_auto_delete(
    hub,
    ctx,
    device_name: str,
    auto_delete: bool,
    project: str = None,
    zone: str = None,
    instance: str = None,
    resource_id: str = None,
    request_id: str = None,
):
    r"""Sets the auto-delete flag for a disk attached to an instance.

    Args:
        device_name(str):
            The device name of the disk to modify. Make a get() request on the instance to view currently attached disks and device names.

        auto_delete(bool):
            Whether to auto-delete the disk when the instance is deleted.

        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            Name of the zone for this request.

        instance(str, Optional):
            The instance name for this request.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type="compute.instance",
        method_name="setDiskAutoDelete",
        method_params={
            "ctx": ctx,
            "device_name": device_name,
            "auto_delete": auto_delete,
            "project": project,
            "zone": zone,
            "instance": instance,
            "resource_id": resource_id,
            "request_id": request_id,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def attach_disk(
    hub,
    ctx,
    project: str = None,
    zone: str = None,
    instance: str = None,
    resource_id: str = None,
    request_id: str = None,
    disk_size_gb: str = None,
    auto_delete: bool = None,
    boot: bool = None,
    guest_os_features: List[
        make_dataclass(
            "GuestOsFeature", [("type_", (str, "alias=type"), field(default=None))]
        )
    ] = None,
    source: str = None,
    disk_encryption_key: make_dataclass(
        "CustomerEncryptionKey",
        [
            ("kms_key_service_account", str, field(default=None)),
            ("sha256", str, field(default=None)),
            ("rsa_encrypted_key", str, field(default=None)),
            ("kms_key_name", str, field(default=None)),
            ("raw_key", str, field(default=None)),
        ],
    ) = None,
    force_attach: bool = None,
    device_name: str = None,
    initialize_params: make_dataclass(
        "AttachedDiskInitializeParams",
        [
            (
                "resource_manager_tags",
                Dict[str, Any],
                field(default=None),
            ),
            ("source_image", str, field(default=None)),
            ("description", str, field(default=None)),
            ("disk_size_gb", str, field(default=None)),
            ("source_snapshot", str, field(default=None)),
            ("provisioned_iops", str, field(default=None)),
            (
                "source_image_encryption_key",
                make_dataclass(
                    "CustomerEncryptionKey",
                    [
                        (
                            "kms_key_service_account",
                            str,
                            field(default=None),
                        ),
                        ("sha256", str, field(default=None)),
                        ("rsa_encrypted_key", str, field(default=None)),
                        ("kms_key_name", str, field(default=None)),
                        ("raw_key", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("on_update_action", str, field(default=None)),
            (
                "source_snapshot_encryption_key",
                make_dataclass(
                    "CustomerEncryptionKey",
                    [
                        (
                            "kms_key_service_account",
                            str,
                            field(default=None),
                        ),
                        ("sha256", str, field(default=None)),
                        ("rsa_encrypted_key", str, field(default=None)),
                        ("kms_key_name", str, field(default=None)),
                        ("raw_key", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("architecture", str, field(default=None)),
            ("licenses", List[str], field(default=None)),
            ("labels", Dict[str, Any], field(default=None)),
            ("disk_type", str, field(default=None)),
            ("disk_name", str, field(default=None)),
            ("resource_policies", List[str], field(default=None)),
        ],
    ) = None,
    interface: str = None,
    mode: str = None,
    type_: (str, "alias=type") = None,
):
    r"""Attaches an existing Disk resource to an instance. You must first create the disk before you can attach it. It is not possible to create and attach a disk at the same time. For more information, read Adding a persistent disk to your instance.

    Args:
        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            Name of the zone for this request.

        instance(str, Optional):
            The instance name for this request.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).

        auto_delete(bool):
            Whether to auto-delete the disk when the instance is deleted.

        disk_size_gb(str, Optional):
            The size of the disk in GB.

        auto_delete(bool, Optional):
            Specifies whether the disk will be auto-deleted when the instance is deleted (but not when the disk is detached from the instance).

        boot(bool, Optional):
            Indicates that this is a boot disk. The virtual machine will use the first partition of the disk for its root filesystem.

        guest_os_features(List[Dict[str, Any]], Optional):
            A list of features to enable on the guest operating system. Applicable only for bootable images. Read Enabling guest operating system features to see a list of available options.

            * type(str, Optional):
                The ID of a supported feature. To add multiple values, use commas to separate values. Set to one or more of the following values: - VIRTIO_SCSI_MULTIQUEUE - WINDOWS - MULTI_IP_SUBNET - UEFI_COMPATIBLE - GVNIC - SEV_CAPABLE - SUSPEND_RESUME_COMPATIBLE - SEV_SNP_CAPABLE For more information, see Enabling guest operating system features.
                    Enum type. Allowed values:
                        "FEATURE_TYPE_UNSPECIFIED"
                        "GVNIC"
                        "MULTI_IP_SUBNET"
                        "SECURE_BOOT"
                        "SEV_CAPABLE"
                        "UEFI_COMPATIBLE"
                        "VIRTIO_SCSI_MULTIQUEUE"
                        "WINDOWS"

        source(str, Optional):
            Specifies a valid partial or full URL to an existing Persistent Disk resource. When creating a new instance, one of initializeParams.sourceImage or initializeParams.sourceSnapshot or disks.source is required except for local SSD. If desired, you can also attach existing non-root persistent disks using this property. This field is only applicable for persistent disks. Note that for InstanceTemplate, specify the disk name for zonal disk, and the URL for regional disk.

        disk_encryption_key(Dict[str, Any], Optional):
            Encrypts or decrypts a disk using a customer-supplied encryption key. If you are creating a new disk, this field encrypts the new disk using an encryption key that you provide. If you are attaching an existing disk that is already encrypted, this field decrypts the disk using the customer-supplied encryption key. If you encrypt a disk using a customer-supplied key, you must provide the same key again when you attempt to use this resource at a later time. For example, you must provide the key when you create a snapshot or an image from the disk or when you attach the disk to a virtual machine instance. If you do not provide an encryption key, then the disk will be encrypted using an automatically generated key and you do not need to provide a key to use the disk later. Instance templates do not store customer-supplied encryption keys, so you cannot use your own keys to encrypt disks in a managed instance group.

            * kms_key_service_account (str, Optional): The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. For example: "kmsKeyServiceAccount": "name@project_id.iam.gserviceaccount.com/"
            * sha256 (str, Optional): [Output only] The RFC 4648 base64 encoded SHA-256 hash of the customer-supplied encryption key that protects this resource.
            * rsa_encrypted_key (str, Optional): Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rsaEncryptedKey": "ieCx/NcW06PcT7Ep1X6LUTc/hLvUDYyzSZPPVCVPTVEohpeHASqC8uw5TzyO9U+Fka9JFH z0mBibXUInrC/jEk014kCK/NPjYgEMOyssZ4ZINPKxlUh2zn1bV+MCaTICrdmuSBTWlUUiFoD D6PYznLwh8ZNdaheCeZ8ewEXgFQ8V+sDroLaN3Xs3MDTXQEMMoNUXMCZEIpg9Vtp9x2oe==" The key must meet the following requirements before you can provide it to Compute Engine: 1. The key is wrapped using a RSA public key certificate provided by Google. 2. After being wrapped, the key must be encoded in RFC 4648 base64 encoding. Gets the RSA public key certificate provided by Google at: https://cloud-certs.storage.googleapis.com/google-cloud-csek-ingress.pem
            * kms_key_name (str, Optional): The name of the encryption key that is stored in Google Cloud KMS. For example: "kmsKeyName": "projects/kms_project_id/locations/region/keyRings/ key_region/cryptoKeys/key
            * raw_key (str, Optional): Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rawKey": "SGVsbG8gZnJvbSBHb29nbGUgQ2xvdWQgUGxhdGZvcm0="

        force_attach(bool, Optional):
            [Input Only] Whether to force attach the regional disk even if it's currently attached to another instance. If you try to force attach a zonal disk to an instance, you will receive an error.

        device_name(str, Optional):
            Specifies a unique device name of your choice that is reflected into the /dev/disk/by-id/google-* tree of a Linux operating system running within the instance. This name can be used to reference the device for mounting, resizing, and so on, from within the instance. If not specified, the server chooses a default device name to apply to this disk, in the form persistent-disk-x, where x is a number assigned by Google Compute Engine. This field is only applicable for persistent disks.

        initialize_params(Dict[str, Any], Optional):
            [Input Only] Specifies the parameters for a new disk that will be created alongside the new instance. Use initialization parameters to create boot disks or local SSDs attached to the new instance. This property is mutually exclusive with the source property; you can only define one or the other, but not both.
            AttachedDiskInitializeParams: [Input Only] Specifies the parameters for a new disk that will be created alongside the new instance. Use initialization parameters to create boot disks or local SSDs attached to the new instance. This field is persisted and returned for instanceTemplate and not returned in the context of instance. This property is mutually exclusive with the source property; you can only define one or the other, but not both.

            * resource_manager_tags (Dict[str, Any], Optional): Resource manager tags to be bound to the disk. Tag keys and values have the same definition as resource manager tags. Keys must be in the format `tagKeys/{tag_key_id}`, and values are in the format `tagValues/456`. The field is ignored (both PUT & PATCH) when empty.
            * source_image (str, Optional): The source image to create this disk. When creating a new instance, one of initializeParams.sourceImage or initializeParams.sourceSnapshot or disks.source is required except for local SSD. To create a disk with one of the public operating system images, specify the image by its family name. For example, specify family/debian-9 to use the latest Debian 9 image: projects/debian-cloud/global/images/family/debian-9 Alternatively, use a specific version of a public operating system image: projects/debian-cloud/global/images/debian-9-stretch-vYYYYMMDD To create a disk with a custom image that you created, specify the image name in the following format: global/images/my-custom-image You can also specify a custom image by its image family, which returns the latest version of the image in that family. Replace the image name with family/family-name: global/images/family/my-image-family If the source image is deleted later, this field will not be set.
            * description (str, Optional): An Optional description. Provide this property when creating the disk.
            * disk_size_gb (str, Optional): Specifies the size of the disk in base-2 GB. The size must be at least 10 GB. If you specify a sourceImage, which is required for boot disks, the default size is the size of the sourceImage. If you do not specify a sourceImage, the default disk size is 500 GB.
            * source_snapshot (str, Optional): The source snapshot to create this disk. When creating a new instance, one of initializeParams.sourceSnapshot or initializeParams.sourceImage or disks.source is required except for local SSD. To create a disk with a snapshot that you created, specify the snapshot name in the following format: global/snapshots/my-backup If the source snapshot is deleted later, this field will not be set.
            * provisioned_iops (str, Optional): Indicates how many IOPS to provision for the disk. This sets the number of I/O operations per second that the disk can handle. Values must be between 10,000 and 120,000. For more details, see the Extreme persistent disk documentation.
            * source_image_encryption_key (Dict[str, Any], Optional): The customer-supplied encryption key of the source image. Required if the source image is protected by a customer-supplied encryption key. InstanceTemplate and InstancePropertiesPatch do not store customer-supplied encryption keys, so you cannot create disks for instances in a managed instance group if the source images are encrypted with your own keys.
                * kms_key_service_account (str, Optional): The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. For example: "kmsKeyServiceAccount": "name@project_id.iam.gserviceaccount.com/"
                * sha256 (str, Optional): [Output only] The RFC 4648 base64 encoded SHA-256 hash of the customer-supplied encryption key that protects this resource.
                * rsa_encrypted_key (str, Optional): Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rsaEncryptedKey": "ieCx/NcW06PcT7Ep1X6LUTc/hLvUDYyzSZPPVCVPTVEohpeHASqC8uw5TzyO9U+Fka9JFH z0mBibXUInrC/jEk014kCK/NPjYgEMOyssZ4ZINPKxlUh2zn1bV+MCaTICrdmuSBTWlUUiFoD D6PYznLwh8ZNdaheCeZ8ewEXgFQ8V+sDroLaN3Xs3MDTXQEMMoNUXMCZEIpg9Vtp9x2oe==" The key must meet the following requirements before you can provide it to Compute Engine: 1. The key is wrapped using a RSA public key certificate provided by Google. 2. After being wrapped, the key must be encoded in RFC 4648 base64 encoding. Gets the RSA public key certificate provided by Google at: https://cloud-certs.storage.googleapis.com/google-cloud-csek-ingress.pem
                * kms_key_name (str, Optional): The name of the encryption key that is stored in Google Cloud KMS. For example: "kmsKeyName": "projects/kms_project_id/locations/region/keyRings/ key_region/cryptoKeys/key
                * raw_key (str, Optional): Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rawKey": "SGVsbG8gZnJvbSBHb29nbGUgQ2xvdWQgUGxhdGZvcm0="
            * on_update_action (str, Optional):
                Specifies which action to take on instance update with this disk. Default is to use the existing disk.
                    Enum type. Allowed values:
                        "RECREATE_DISK" - Always recreate the disk.
                        "RECREATE_DISK_IF_SOURCE_CHANGED" - Recreate the disk if source (image, snapshot) of this disk is different from source of existing disk.
                        "USE_EXISTING_DISK" - Use the existing disk, this is the default behaviour.

            * source_snapshot_encryption_key (Dict[str, Any], Optional): The customer-supplied encryption key of the source snapshot.
                * kms_key_service_account (str, Optional): The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. For example: "kmsKeyServiceAccount": "name@project_id.iam.gserviceaccount.com/"
                * sha256 (str, Optional): [Output only] The RFC 4648 base64 encoded SHA-256 hash of the customer-supplied encryption key that protects this resource.
                * rsa_encrypted_key (str, Optional): Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rsaEncryptedKey": "ieCx/NcW06PcT7Ep1X6LUTc/hLvUDYyzSZPPVCVPTVEohpeHASqC8uw5TzyO9U+Fka9JFH z0mBibXUInrC/jEk014kCK/NPjYgEMOyssZ4ZINPKxlUh2zn1bV+MCaTICrdmuSBTWlUUiFoD D6PYznLwh8ZNdaheCeZ8ewEXgFQ8V+sDroLaN3Xs3MDTXQEMMoNUXMCZEIpg9Vtp9x2oe==" The key must meet the following requirements before you can provide it to Compute Engine: 1. The key is wrapped using a RSA public key certificate provided by Google. 2. After being wrapped, the key must be encoded in RFC 4648 base64 encoding. Gets the RSA public key certificate provided by Google at: https://cloud-certs.storage.googleapis.com/google-cloud-csek-ingress.pem
                * kms_key_name (str, Optional): The name of the encryption key that is stored in Google Cloud KMS. For example: "kmsKeyName": "projects/kms_project_id/locations/region/keyRings/ key_region/cryptoKeys/key
                * raw_key (str, Optional): Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rawKey": "SGVsbG8gZnJvbSBHb29nbGUgQ2xvdWQgUGxhdGZvcm0="
            * architecture (str, Optional):
                The architecture of the attached disk. Valid values are arm64 or x86_64.
                    Enum type. Allowed values:
                        "ARCHITECTURE_UNSPECIFIED" - Default value indicating Architecture is not set.
                        "ARM64" - Machines with architecture ARM64
                        "X86_64" - Machines with architecture X86_64
            * licenses (List[str], Optional): A list of publicly visible licenses. Reserved for Google's use.
            * labels (Dict[str, Any], Optional): Labels to apply to this disk. These can be later modified by the disks.setLabels method. This field is only applicable for persistent disks.
            * disk_type (str, Optional): Specifies the disk type to use to create the instance. If not specified, the default is pd-standard, specified using the full URL. For example: https://www.googleapis.com/compute/v1/projects/project/zones/zone /diskTypes/pd-standard For a full list of acceptable values, see Persistent disk types. If you specify this field when creating a VM, you can provide either the full or partial URL. For example, the following values are valid: - https://www.googleapis.com/compute/v1/projects/project/zones/zone /diskTypes/diskType - projects/project/zones/zone/diskTypes/diskType - zones/zone/diskTypes/diskType If you specify this field when creating or updating an instance template or all-instances configuration, specify the type of the disk, not the URL. For example: pd-standard.
            * disk_name (str, Optional): Specifies the disk name. If not specified, the default is to use the name of the instance. If a disk with the same name already exists in the given region, the existing disk is attached to the new instance and the new disk is not created.
            * resource_policies (List[str], Optional): Resource policies applied to this disk for automatic snapshot creations. Specified using the full or partial URL. For instance template, specify only the resource policy name.

        interface(str, Optional):
            Specifies the disk interface to use for attaching this disk, which is either SCSI or NVME. For most machine types, the default is SCSI. Local SSDs can use either NVME or SCSI. In certain configurations, persistent disks can use NVMe. For more information, see About persistent disks.
                Enum type. Allowed values:
                    "NVME"
                    "SCSI"

        mode(str, Optional):
            The mode in which to attach this disk, either READ_WRITE or READ_ONLY. If not specified, the default is to attach the disk in READ_WRITE mode.
                Enum type. Allowed values:
                    "READ_ONLY" - Attaches this disk in read-only mode. Multiple virtual machines can use a disk in read-only mode at a time.
                    "READ_WRITE" - *[Default]* Attaches this disk in read-write mode. Only one virtual machine at a time can be attached to a disk in read-write mode.

        type(str, Optional):
            Specifies the type of the disk, either SCRATCH or PERSISTENT. If not specified, the default is PERSISTENT.
                Enum type. Allowed values:
                    "PERSISTENT"
                    "SCRATCH"
    """
    request_body = {
        "disk_size_gb": disk_size_gb,
        "auto_delete": auto_delete,
        "boot": boot,
        "guest_os_features": guest_os_features,
        "source": source,
        "disk_encryption_key": disk_encryption_key,
        "force_attach": force_attach,
        "device_name": device_name,
        "initialize_params": initialize_params,
        "interface": interface,
        "mode": mode,
        "type": type_,
    }

    execution_context = ExecutionContext(
        resource_type="compute.instance",
        method_name="attachDisk",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "body": request_body,
            "forceAttach": force_attach,
            "requestId": request_id,
            "project": project,
            "zone": zone,
            "instance": instance,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def detach_disk(
    hub,
    ctx,
    device_name: str,
    project: str = None,
    zone: str = None,
    instance: str = None,
    resource_id: str = None,
    request_id: str = None,
):
    r"""Detaches a disk from an instance.

    Args:
        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            Name of the zone for this request.

        instance(str, Optional):
            The instance name for this request.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).

        device_name(str):
            The device name of the disk to detach. Make a get() request on the instance to view currently attached disks and device names.
    """
    execution_context = ExecutionContext(
        resource_type="compute.instance",
        method_name="detachDisk",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "deviceName": device_name,
            "requestId": request_id,
            "project": project,
            "zone": zone,
            "instance": instance,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def get_effective_firewalls(
    hub,
    ctx,
    project: str = None,
    zone: str = None,
    instance: str = None,
    resource_id: str = None,
    network_interface: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""Returns effective firewalls applied to an interface of the instance.

    Args:
        network_interface(str):
            The name of the network interface to get the effective firewalls.

        project(str, Optional):
            Project ID for this request. Defaults to None.

        zone(str, Optional):
            Name of the zone for this request. Defaults to None.

        instance(str, Optional):
            The instance name for this request. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).  Defaults to None.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance.get_effective_firewalls
              - kwargs:
                  project: project-name
                  zone: zone-name
                  name: instance-name
                  network_interface: network-interface-name
    """
    execution_context = ExecutionContext(
        resource_type="compute.instance",
        method_name="getEffectiveFirewalls",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "zone": zone,
            "instance": instance,
            "network_interface": network_interface,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def set_shielded_instance_integrity_policy(
    hub,
    ctx,
    update_auto_learn_policy: bool,
    project: str = None,
    zone: str = None,
    instance: str = None,
    resource_id: str = None,
    request_id: str = None,
):
    r"""Sets the Shielded Instance integrity policy for an instance. You can only use this method on a running instance. This method supports PATCH semantics and uses the JSON merge patch format and processing rules.

    Args:
        update_auto_learn_policy(bool):
            Updates the integrity policy baseline using the measurements from the VM instance's most recent boot.

        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            Name of the zone for this request.

        instance(str, Optional):
            The instance name for this request.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
    """
    request_body = {"update_auto_learn_policy": update_auto_learn_policy}
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)
    execution_context = ExecutionContext(
        resource_type="compute.instance",
        method_name="setShieldedInstanceIntegrityPolicy",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "request_id": request_id,
            "project": project,
            "zone": zone,
            "instance": instance,
            "body": request_body,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def update_shielded_instance_config(
    hub,
    ctx,
    enable_secure_boot: bool,
    enable_vtpm: bool,
    enable_integrity_monitoring: bool,
    project: str = None,
    zone: str = None,
    instance: str = None,
    resource_id: str = None,
    request_id: str = None,
):
    r"""Updates the Shielded Instance config for an instance. You can only use this method on a stopped instance. This method supports PATCH semantics and uses the JSON merge patch format and processing rules.

    Args:
        enable_secure_boot(bool):
            Defines whether the instance has Secure Boot enabled. Disabled by default.

        enable_vtpm(bool):
            Defines whether the instance has the vTPM enabled. Enabled by default.

        enable_integrity_monitoring(bool):
            Defines whether the instance has integrity monitoring enabled. Enabled by default.

        project(str, Optional):
            Project ID for this request.

        zone(str, Optional):
            Name of the zone for this request.

        instance(str, Optional):
            The instance name for this request.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).
    """
    request_body = {
        "enable_secure_boot": enable_secure_boot,
        "enable_vtpm": enable_vtpm,
        "enable_integrity_monitoring": enable_integrity_monitoring,
    }
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)
    execution_context = ExecutionContext(
        resource_type="compute.instance",
        method_name="updateShieldedInstanceConfig",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "request_id": request_id,
            "project": project,
            "zone": zone,
            "instance": instance,
            "body": request_body,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def start(
    hub,
    ctx,
    resource_id: str = None,
    project: str = None,
    zone: str = None,
    instance: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""Starts an instance that was stopped using the instances().stop method. For more information, see Restart an instance.

    Args:
        project(str, Optional):
            Project ID for this request. Defaults to None.

        zone(str, Optional):
            Name of the zone for this request. Defaults to None.

        instance(str, Optional):
            Name of the instance resource to start. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).  Defaults to None.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance.start
              - kwargs:
                  project: project-name
                  zone: zone-name
                  instance: instance-name
    """
    execution_context = ExecutionContext(
        resource_type="compute.instance",
        method_name="start",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "zone": zone,
            "instance": instance,
            "request_id": request_id,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def stop(
    hub,
    ctx,
    resource_id: str = None,
    project: str = None,
    zone: str = None,
    instance: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""Stops a running instance, shutting it down cleanly, and allows you to restart the instance at a later time. Stopped instances do not incur VM usage charges while they are stopped. However, resources that the VM is using, such as persistent disks and static IP addresses, will continue to be charged until they are deleted. For more information, see Stopping an instance.

    Args:
        project(str, Optional):
            Project ID for this request. Defaults to None.

        zone(str, Optional):
            Name of the zone for this request. Defaults to None.

        instance(str, Optional):
            Name of the instance resource to stop. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).  Defaults to None.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance.stop
              - kwargs:
                  project: project-name
                  zone: zone-name
                  instance: instance-name
    """
    execution_context = ExecutionContext(
        resource_type="compute.instance",
        method_name="stop",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "zone": zone,
            "instance": instance,
            "request_id": request_id,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def resume(
    hub,
    ctx,
    resource_id: str = None,
    project: str = None,
    zone: str = None,
    instance: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""Resumes an instance that was suspended using the instances().suspend method.

    Args:
        project(str, Optional):
            Project ID for this request. Defaults to None.

        zone(str, Optional):
            Name of the zone for this request. Defaults to None.

        instance(str, Optional):
            Name of the instance resource to resume. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).  Defaults to None.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance.resume
              - kwargs:
                  project: project-name
                  zone: zone-name
                  instance: instance-name
    """
    execution_context = ExecutionContext(
        resource_type="compute.instance",
        method_name="resume",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "zone": zone,
            "instance": instance,
            "request_id": request_id,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def suspend(
    hub,
    ctx,
    resource_id: str = None,
    project: str = None,
    zone: str = None,
    instance: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""This method suspends a running instance, saving its state to persistent storage, and allows you to resume the instance at a later time. Suspended instances have no compute costs (cores or RAM), and incur only storage charges for the saved VM memory and localSSD data. Any charged resources the virtual machine was using, such as persistent disks and static IP addresses, will continue to be charged while the instance is suspended. For more information, see Suspending and resuming an instance.

    Args:
        project(str, Optional):
            Project ID for this request. Defaults to None.

        zone(str, Optional):
            Name of the zone for this request. Defaults to None.

        instance(str, Optional):
            Name of the instance resource to suspend. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000).  Defaults to None.

    Examples:
        .. code-block:: sls

            random-name:
              exec.run:
              - path: gcp.compute.instance.resume
              - kwargs:
                  project: project-name
                  zone: zone-name
                  instance: instance-name
    """
    execution_context = ExecutionContext(
        resource_type="compute.instance",
        method_name="suspend",
        method_params={
            "ctx": ctx,
            "resource_id": resource_id,
            "project": project,
            "zone": zone,
            "instance": instance,
            "request_id": request_id,
        },
    )
    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)
