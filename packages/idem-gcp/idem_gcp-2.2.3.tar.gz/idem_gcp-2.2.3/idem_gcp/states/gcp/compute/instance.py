"""Google Cloud Platform compute instances state module.

Copyright (c) 2022 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0

"""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from dict_tools.typing import Computed

from idem_gcp.tool.gcp.state_operation_utils import StateOperations
from idem_gcp.tool.gcp.utils import zonal_absent

# prevent commit hook from removing the import
absent = zonal_absent

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    zone: str,
    project: str = None,
    service_accounts: List[
        make_dataclass(
            "ServiceAccount",
            [
                ("scopes", List[str], field(default=None)),
                ("email", str, field(default=None)),
            ],
        )
    ] = None,
    label_fingerprint: str = None,
    fingerprint: str = None,
    advanced_machine_features: make_dataclass(
        "AdvancedMachineFeatures",
        [
            ("enable_nested_virtualization", bool, field(default=None)),
            ("visible_core_count", int, field(default=None)),
            ("enable_uefi_networking", bool, field(default=None)),
            ("threads_per_core", int, field(default=None)),
        ],
    ) = None,
    can_ip_forward: bool = None,
    network_interfaces: List[
        make_dataclass(
            "NetworkInterface",
            [
                ("kind", str, field(default=None)),
                ("network", str, field(default=None)),
                ("stack_type", str, field(default=None)),
                ("name", str, field(default=None)),
                ("subnetwork", str, field(default=None)),
                ("queue_count", int, field(default=None)),
                (
                    "ipv6_access_configs",
                    List[
                        make_dataclass(
                            "AccessConfig",
                            [
                                ("network_tier", str, field(default=None)),
                                (
                                    "external_ipv6_prefix_length",
                                    int,
                                    field(default=None),
                                ),
                                ("name", str, field(default=None)),
                                ("kind", str, field(default=None)),
                                ("external_ipv6", str, field(default=None)),
                                ("type_", (str, "alias=type"), field(default=None)),
                                ("set_public_ptr", bool, field(default=None)),
                                ("public_ptr_domain_name", str, field(default=None)),
                                ("nat_ip", str, field(default=None)),
                            ],
                        )
                    ],
                    field(default=None),
                ),
                ("internal_ipv6_prefix_length", int, field(default=None)),
                ("fingerprint", str, field(default=None)),
                (
                    "alias_ip_ranges",
                    List[
                        make_dataclass(
                            "AliasIpRange",
                            [
                                ("ip_cidr_range", str, field(default=None)),
                                ("subnetwork_range_name", str, field(default=None)),
                            ],
                        )
                    ],
                    field(default=None),
                ),
                ("ipv6_access_type", str, field(default=None)),
                ("network_ip", str, field(default=None)),
                ("nic_type", str, field(default=None)),
                (
                    "access_configs",
                    List[
                        make_dataclass(
                            "AccessConfig",
                            [
                                ("network_tier", str, field(default=None)),
                                (
                                    "external_ipv6_prefix_length",
                                    int,
                                    field(default=None),
                                ),
                                ("name", str, field(default=None)),
                                ("kind", str, field(default=None)),
                                ("external_ipv6", str, field(default=None)),
                                ("type_", (str, "alias=type"), field(default=None)),
                                ("set_public_ptr", bool, field(default=None)),
                                ("public_ptr_domain_name", str, field(default=None)),
                                ("nat_ip", str, field(default=None)),
                            ],
                        )
                    ],
                    field(default=None),
                ),
                ("ipv6_address", str, field(default=None)),
            ],
        )
    ] = None,
    labels: Dict[str, Any] = None,
    display_device: make_dataclass(
        "DisplayDevice", [("enable_display", bool, field(default=None))]
    ) = None,
    source_machine_image: str = None,
    resource_policies: List[str] = None,
    status: str = None,
    tags: make_dataclass(
        "Tags",
        [
            ("fingerprint", str, field(default=None)),
            ("items", List[str], field(default=None)),
        ],
    ) = None,
    key_revocation_action_type: str = None,
    scheduling: make_dataclass(
        "Scheduling",
        [
            ("on_host_maintenance", str, field(default=None)),
            ("preemptible", bool, field(default=None)),
            ("min_node_cpus", int, field(default=None)),
            ("automatic_restart", bool, field(default=None)),
            (
                "node_affinities",
                List[
                    make_dataclass(
                        "SchedulingNodeAffinity",
                        [
                            ("operator", str, field(default=None)),
                            ("values", List[str], field(default=None)),
                            ("key", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("instance_termination_action", str, field(default=None)),
            ("provisioning_model", str, field(default=None)),
            ("location_hint", str, field(default=None)),
        ],
    ) = None,
    private_ipv6_google_access: str = None,
    description: str = None,
    guest_accelerators: List[
        make_dataclass(
            "AcceleratorConfig",
            [
                ("accelerator_count", int, field(default=None)),
                ("accelerator_type", str, field(default=None)),
            ],
        )
    ] = None,
    confidential_instance_config: make_dataclass(
        "ConfidentialInstanceConfig",
        [("enable_confidential_compute", bool, field(default=None))],
    ) = None,
    shielded_instance_config: make_dataclass(
        "ShieldedInstanceConfig",
        [
            ("enable_vtpm", bool, field(default=None)),
            ("enable_secure_boot", bool, field(default=None)),
            ("enable_integrity_monitoring", bool, field(default=None)),
        ],
    ) = None,
    source_machine_image_encryption_key: make_dataclass(
        "CustomerEncryptionKey",
        [
            ("kms_key_service_account", str, field(default=None)),
            ("sha256", str, field(default=None)),
            ("rsa_encrypted_key", str, field(default=None)),
            ("kms_key_name", str, field(default=None)),
            ("raw_key", str, field(default=None)),
        ],
    ) = None,
    disks: List[
        make_dataclass(
            "AttachedDisk",
            [
                ("disk_size_gb", str, field(default=None)),
                ("auto_delete", bool, field(default=None)),
                ("boot", bool, field(default=None)),
                (
                    "guest_os_features",
                    List[
                        make_dataclass(
                            "GuestOsFeature",
                            [("type_", (str, "alias=type"), field(default=None))],
                        )
                    ],
                    field(default=None),
                ),
                ("source", str, field(default=None)),
                (
                    "disk_encryption_key",
                    make_dataclass(
                        "CustomerEncryptionKey",
                        [
                            ("kms_key_service_account", str, field(default=None)),
                            ("sha256", str, field(default=None)),
                            ("rsa_encrypted_key", str, field(default=None)),
                            ("kms_key_name", str, field(default=None)),
                            ("raw_key", str, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                ("force_attach", bool, field(default=None)),
                ("architecture", str, field(default=None)),
                ("device_name", str, field(default=None)),
                (
                    "shielded_instance_initial_state",
                    make_dataclass(
                        "InitialStateConfig",
                        [
                            (
                                "keks",
                                List[
                                    make_dataclass(
                                        "FileContentBuffer",
                                        [
                                            ("file_type", str, field(default=None)),
                                            ("content", str, field(default=None)),
                                        ],
                                    )
                                ],
                                field(default=None),
                            ),
                            (
                                "dbs",
                                List[
                                    make_dataclass(
                                        "FileContentBuffer",
                                        [
                                            ("file_type", str, field(default=None)),
                                            ("content", str, field(default=None)),
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
                                            ("file_type", str, field(default=None)),
                                            ("content", str, field(default=None)),
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
                                        ("file_type", str, field(default=None)),
                                        ("content", str, field(default=None)),
                                    ],
                                ),
                                field(default=None),
                            ),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "initialize_params",
                    make_dataclass(
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
                    ),
                    field(default=None),
                ),
                ("kind", str, field(default=None)),
                ("index", int, field(default=None)),
                ("interface", str, field(default=None)),
                ("licenses", List[str], field(default=None)),
                ("mode", str, field(default=None)),
                ("type_", (str, "alias=type"), field(default=None)),
            ],
        )
    ] = None,
    hostname: str = None,
    network_performance_config: make_dataclass(
        "NetworkPerformanceConfig",
        [("total_egress_bandwidth_tier", str, field(default=None))],
    ) = None,
    params: make_dataclass(
        "InstanceParams",
        [("resource_manager_tags", Dict[str, Any], field(default=None))],
    ) = None,
    deletion_protection: bool = None,
    metadata: make_dataclass(
        "Metadata",
        [
            (
                "items",
                List[
                    make_dataclass(
                        "MetadataItemsProperties",
                        [
                            ("key", str, field(default=None)),
                            ("value", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("kind", str, field(default=None)),
            ("fingerprint", str, field(default=None)),
        ],
    ) = None,
    shielded_instance_integrity_policy: make_dataclass(
        "ShieldedInstanceIntegrityPolicy",
        [("update_auto_learn_policy", bool, field(default=None))],
    ) = None,
    reservation_affinity: make_dataclass(
        "ReservationAffinity",
        [
            ("key", str, field(default=None)),
            ("values", List[str], field(default=None)),
            ("consume_reservation_type", str, field(default=None)),
        ],
    ) = None,
    min_cpu_platform: str = None,
    machine_type: str = None,
    source_instance_template: str = None,
    request_id: str = None,
    minimal_action: str = None,
    most_disruptive_allowed_action: str = None,
    resource_id: str = None,
    id_: (Computed[str], "alias=id") = None,
) -> Dict[str, Any]:
    """Create or update a compute instance resource.

    Creates an instance resource in the specified project using the data included in the request.
    or
    Updates an instance only if the necessary resources are available. This method can update only a specific set of instance properties. See Updating a running instance for a list of updatable instance properties.

    Args:
        name(str):
            An Idem name of the resource.

        service_accounts(List[Dict[str, Any]], Optional):
            A list of service accounts, with their specified scopes, authorized for this instance. Only one service account per VM instance is supported. Service accounts generate access tokens that can be accessed through the metadata server and used to authenticate applications on the instance. See Service Accounts for more information. Defaults to None.

            * scopes(List[str], Optional):
                The list of scopes to be made available for this service account.
            * email(str, Optional):
                Email address of the service account.

        label_fingerprint(str, Optional):
            A fingerprint for this request, which is essentially a hash of the label's contents and used for optimistic locking. The fingerprint is initially generated by Compute Engine and changes after every request to modify or update labels. You must always provide an up-to-date fingerprint hash in order to update or change labels. To see the latest fingerprint, make get() request to the instance. Defaults to None.

        fingerprint(str, Optional):
            Specifies a fingerprint for this resource, which is essentially a hash of the instance's contents and used for optimistic locking. The fingerprint is initially generated by Compute Engine and changes after every request to modify or update the instance. You must always provide an up-to-date fingerprint hash in order to update the instance. To see the latest fingerprint, make get() request to the instance. Defaults to None.

        advanced_machine_features(Dict[str, Any], Optional):
            Specifies options for controlling advanced machine features. Options that would traditionally be configured in a BIOS belong here. Features that require operating system support may have corresponding entries in the GuestOsFeatures of an Image (e.g., whether or not the OS in the Image supports nested virtualization being enabled or disabled). Defaults to None.

            * enable_nested_virtualization (bool, Optional):
                Whether to enable nested virtualization or not (default is false).
            * visible_core_count (int, Optional):
                The number of physical cores to expose to an instance. Multiply by the number of threads per core to compute the total number of virtual CPUs to expose to the instance. If unset, the number of cores is inferred from the instance's nominal CPU count and the underlying platform's SMT width.
            * enable_uefi_networking (bool, Optional):
                Whether to enable UEFI networking for instance creation.
            * threads_per_core (int, Optional):
                The number of threads per physical core. To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed.

        can_ip_forward(bool, Optional):
            Allows this instance to send and receive packets with non-matching destination or source IPs. This is required if you plan to use this instance to forward routes. For more information, see Enabling IP Forwarding . Defaults to None.

        network_interfaces(List[Dict[str, Any]], Optional):
            An array of network configurations for this instance. These specify how interfaces are configured to interact with other network services, such as connecting to the internet. Multiple interfaces are supported per instance. Defaults to None.

            * kind (str, Optional):
                [Output Only] Type of the resource. Always compute#networkInterface for network interfaces.
            * network (str, Optional):
                URL of the VPC network resource for this instance. When creating an instance, if neither the network nor the subnetwork is specified, the default network global/networks/default is used. If the selected project doesn't have the default network, you must specify a network or subnet. If the network is not specified but the subnetwork is specified, the network is inferred. If you specify this property, you can specify the network as a full or partial URL. For example, the following are all valid URLs:

                - https://www.googleapis.com/compute/v1/projects/project/global/networks/network
                - projects/project/global/networks/network
                - global/networks/default
            * stack_type (str, Optional):
                The stack type for this network interface to identify whether the IPv6 feature is enabled or not. If not specified, IPV4_ONLY will be used. This field can be both set at instance creation and update network interface operations.
                Enum type. Allowed values:
                    "IPV4_IPV6" - The network interface can have both IPv4 and IPv6 addresses.
                    "IPV4_ONLY" - The network interface will be assigned IPv4 address.
            * name (str, Optional):
                [Output Only] The name of the network interface, which is generated by the server. For a VM, the network interface uses the nicN naming format. Where N is a value between 0 and 7. The default interface value is nic0.
            * subnetwork (str, Optional):
                The URL of the Subnetwork resource for this instance. If the network resource is in legacy mode, do not specify this field. If the network is in auto subnet mode, specifying the subnetwork is optional. If the network is in custom subnet mode, specifying the subnetwork is required. If you specify this field, you can specify the subnetwork as a full or partial URL. For example, the following are all valid URLs:

                - https://www.googleapis.com/compute/v1/projects/project/regions/region/subnetworks/subnetwork
                - regions/region/subnetworks/subnetwork
            * queue_count (int, Optional):
                The networking queue count that's specified by users for the network interface. Both Rx and Tx queues will be set to this number. It'll be empty if not specified by the users.
            * ipv6_access_configs (List[Dict[str, Any]], Optional):
                An array of IPv6 access configurations for this interface. Currently, only one IPv6 access config, DIRECT_IPV6, is supported. If there is no ipv6AccessConfig specified, then this instance will have no external IPv6 Internet access.

                * network_tier (str, Optional):
                    This signifies the networking tier used for configuring this access configuration and can only take the following values: PREMIUM, STANDARD. If an AccessConfig is specified without a valid external IP address, an ephemeral IP will be created with this networkTier. If an AccessConfig with a valid external IP address is specified, it must match that of the networkTier associated with the Address resource owning that IP.
                    Enum type. Allowed values:
                        "FIXED_STANDARD" - Public internet quality with fixed bandwidth.
                        "PREMIUM" - High quality, Google-grade network tier, support for all networking products.
                        "STANDARD" - Public internet quality, only limited support for other networking products.
                        "STANDARD_OVERRIDES_FIXED_STANDARD" - (Output only) Temporary tier for FIXED_STANDARD when fixed standard tier is expired or not configured.
                * external_ipv6_prefix_length (int, Optional):
                    The prefix length of the external IPv6 range.
                * name (str, Optional):
                    The name of this access configuration. The default and recommended name is External NAT, but you can use any arbitrary string, such as My external IP or Network Access.
                * kind (str, Optional):
                    [Output Only] Type of the resource. Always compute#accessConfig for access configs.
                * external_ipv6 (str, Optional):
                    The first IPv6 address of the external IPv6 range associated with this instance, prefix length is stored in externalIpv6PrefixLength in ipv6AccessConfig. The field is output only, an IPv6 address from a subnetwork associated with the instance will be allocated dynamically.
                * type (str, Optional):
                    The type of configuration. The default and only option is ONE_TO_ONE_NAT.
                    Enum type. Allowed values:
                        "DIRECT_IPV6"
                        "ONE_TO_ONE_NAT"
                * set_public_ptr (bool, Optional):
                    Specifies whether a public DNS 'PTR' record should be created to map the external IP address of the instance to a DNS domain name. This field is not used in ipv6AccessConfig. A default PTR record will be created if the VM has external IPv6 range associated.
                * public_ptr_domain_name (str, Optional):
                    The DNS domain name for the public PTR record. You can set this field only if the `setPublicPtr` field is enabled in accessConfig. If this field is unspecified in ipv6AccessConfig, a default PTR record will be createc for first IP in associated external IPv6 range.
                * nat_ip (str, Optional):
                    An external IP address associated with this instance. Specify an unused static external IP address available to the project or leave this field undefined to use an IP from a shared ephemeral IP address pool. If you specify a static external IP address, it must live in the same region as the zone of the instance.

            * internal_ipv6_prefix_length (int, Optional):
                The prefix length of the primary internal IPv6 range.
            * fingerprint (str, Optional):
                Fingerprint hash of contents stored in this network interface. This field will be ignored when inserting an Instance or adding a NetworkInterface. An up-to-date fingerprint must be provided in order to update the NetworkInterface. The request will fail with error 400 Bad Request if the fingerprint is not provided, or 412 Precondition Failed if the fingerprint is out of date.
            * alias_ip_ranges (List[Dict[str, Any]], Optional):
                An array of alias IP ranges for this network interface. You can only specify this field for network interfaces in VPC networks.

                * ip_cidr_range (str, Optional):
                    The IP alias ranges to allocate for this interface. This IP CIDR range must belong to the specified subnetwork and cannot contain IP addresses reserved by system or used by other network interfaces. This range may be a single IP address (such as 10.2.3.4), a netmask (such as /24) or a CIDR-formatted string (such as 10.1.2.0/24).
                * subnetwork_range_name (str, Optional):
                    The name of a subnetwork secondary IP range from which to allocate an IP alias range. If not specified, the primary range of the subnetwork is used.

            * ipv6_access_type (str, Optional):
                [Output Only] One of EXTERNAL, INTERNAL to indicate whether the IP can be accessed from the Internet. This field is always inherited from its subnetwork. Valid only if stackType is IPV4_IPV6.
                Enum type. Allowed values:
                    "EXTERNAL" - This network interface can have external IPv6.
                    "INTERNAL" - This network interface can have internal IPv6.

            * network_ip (str, Optional):
                An IPv4 internal IP address to assign to the instance for this network interface. If not specified by the user, an unused internal IP is assigned by the system.

            * nic_type (str, Optional):
                The type of vNIC to be used on this interface. This may be gVNIC or VirtioNet.
                Enum type. Allowed values:
                    "GVNIC" - GVNIC
                    "UNSPECIFIED_NIC_TYPE" - No type specified.
                    "VIRTIO_NET" - VIRTIO

            * access_configs (List[Dict[str, Any]], Optional):
                An array of configurations for this interface. Currently, only one access config, ONE_TO_ONE_NAT, is supported. If there are no accessConfigs specified, then this instance will have no external internet access.

                * network_tier (str, Optional):
                    This signifies the networking tier used for configuring this access configuration and can only take the following values: PREMIUM, STANDARD. If an AccessConfig is specified without a valid external IP address, an ephemeral IP will be created with this networkTier. If an AccessConfig with a valid external IP address is specified, it must match that of the networkTier associated with the Address resource owning that IP.
                    Enum type. Allowed values:
                        "FIXED_STANDARD" - Public internet quality with fixed bandwidth.
                        "PREMIUM" - High quality, Google-grade network tier, support for all networking products.
                        "STANDARD" - Public internet quality, only limited support for other networking products.
                        "STANDARD_OVERRIDES_FIXED_STANDARD" - (Output only) Temporary tier for FIXED_STANDARD when fixed standard tier is expired or not configured.
                * external_ipv6_prefix_length (int, Optional):
                    The prefix length of the external IPv6 range.
                * name (str, Optional):
                    The name of this access configuration. The default and recommended name is External NAT, but you can use any arbitrary string, such as My external IP or Network Access.
                * kind (str, Optional):
                    [Output Only] Type of the resource. Always compute#accessConfig for access configs.
                * external_ipv6 (str, Optional):
                    The first IPv6 address of the external IPv6 range associated with this instance, prefix length is stored in externalIpv6PrefixLength in ipv6AccessConfig. The field is output only, an IPv6 address from a subnetwork associated with the instance will be allocated dynamically.
                * type (str, Optional):
                    The type of configuration. The default and only option is ONE_TO_ONE_NAT.
                    Enum type. Allowed values:
                        "DIRECT_IPV6"
                        "ONE_TO_ONE_NAT"
                * set_public_ptr (bool, Optional):
                    Specifies whether a public DNS 'PTR' record should be created to map the external IP address of the instance to a DNS domain name. This field is not used in ipv6AccessConfig. A default PTR record will be created if the VM has external IPv6 range associated.
                * public_ptr_domain_name (str, Optional):
                    The DNS domain name for the public PTR record. You can set this field only if the `setPublicPtr` field is enabled in accessConfig. If this field is unspecified in ipv6AccessConfig, a default PTR record will be createc for first IP in associated external IPv6 range.
                * nat_ip (str, Optional):
                    An external IP address associated with this instance. Specify an unused static external IP address available to the project or leave this field undefined to use an IP from a shared ephemeral IP address pool. If you specify a static external IP address, it must live in the same region as the zone of the instance.

            * ipv6_address (str, Optional):
                An IPv6 internal network address for this network interface.

        labels(Dict[str, Any], Optional):
            Labels to apply to this instance. These can be later modified by the setLabels method. Defaults to None.

        display_device(Dict[str, Any], Optional):
            Enables display device for the instance.
            DisplayDevice: A set of Display Device options. Defaults to None.

            * enable_display (bool, Optional):
                Defines whether the instance has Display enabled.

        resource_policies(List[str], Optional):
            Resource policies applied to this instance. Defaults to None.

        status(str, Optional):
            The status of the instance. One of the following values: PROVISIONING, STAGING, RUNNING, STOPPING, SUSPENDING, SUSPENDED, REPAIRING, and TERMINATED. For more information about the status of the instance, see Instance life cycle.
            Enum type. Allowed values:
                "DEPROVISIONING" - The Nanny is halted and we are performing tear down tasks like network deprogramming, releasing quota, IP, tearing down disks etc.
                "PROVISIONING" - Resources are being allocated for the instance.
                "REPAIRING" - The instance is in repair.
                "RUNNING" - The instance is running.
                "STAGING" - All required resources have been allocated and the instance is being started.
                "STOPPED" - The instance has stopped successfully.
                "STOPPING" - The instance is currently stopping (either being deleted or killed).
                "SUSPENDED" - The instance has suspended.
                "SUSPENDING" - The instance is suspending.
                "TERMINATED" - The instance has stopped (either by explicit action or underlying failure). Defaults to None.

        tags(Dict[str, Any], Optional):
            Tags to apply to this instance. Tags are used to identify valid sources or targets for network firewalls and are specified by the client during instance creation. The tags can be later modified by the setTags method. Each tag within the list must comply with RFC1035. Multiple tags can be specified via the 'tags.items' field.
            Tags: A set of instance tags. Defaults to None.

            * fingerprint (str, Optional):
                Specifies a fingerprint for this request, which is essentially a hash of the tags' contents and used for optimistic locking. The fingerprint is initially generated by Compute Engine and changes after every request to modify or update tags. You must always provide an up-to-date fingerprint hash in order to update or change tags. To see the latest fingerprint, make get() request to the instance.
            * items (List[str], Optional):
                An array of tags. Each tag must be 1-63 characters long, and comply with RFC1035.

        key_revocation_action_type(str, Optional):
            KeyRevocationActionType of the instance. Supported options are "STOP" and "NONE". The default value is "NONE" if it is not specified.
            Enum type. Allowed values:
                "KEY_REVOCATION_ACTION_TYPE_UNSPECIFIED" - Default value. This value is unused.
                "NONE" - Indicates user chose no operation.
                "STOP" - Indicates user chose to opt for VM shutdown on key revocation. Defaults to None.

        scheduling(Dict[str, Any], Optional):
            Sets the scheduling options for this instance.
            Scheduling: Sets the scheduling options for an Instance. Defaults to None.

            * on_host_maintenance (str, Optional):
                Defines the maintenance behavior for this instance. For standard instances, the default behavior is MIGRATE. For preemptible instances, the default and only possible behavior is TERMINATE. For more information, see Set VM host maintenance policy.
                Enum type. Allowed values:
                    "MIGRATE" - *[Default]* Allows Compute Engine to automatically migrate instances out of the way of maintenance events.
                    "TERMINATE" - Tells Compute Engine to terminate and (optionally) restart the instance away from the maintenance activity. If you would like your instance to be restarted, set the automaticRestart flag to true. Your instance may be restarted more than once, and it may be restarted outside the window of maintenance events.
            * preemptible (bool, Optional):
                Defines whether the instance is preemptible. This can only be set during instance creation or while the instance is stopped and therefore, in a `TERMINATED` state. See Instance Life Cycle for more information on the possible instance states.
            * min_node_cpus (int, Optional):
                The minimum number of virtual CPUs this instance will consume when running on a sole-tenant node.
            * automatic_restart (bool, Optional):
                Specifies whether the instance should be automatically restarted if it is terminated by Compute Engine (not terminated by a user). You can only set the automatic restart option for standard instances. Preemptible instances cannot be automatically restarted. By default, this is set to true so an instance is automatically restarted if it is terminated by Compute Engine.
            * node_affinities (List[Dict[str, Any]], Optional):
                A set of node affinity and anti-affinity configurations. Refer to Configuring node affinity for more information. Overrides reservationAffinity.

                * operator (str, Optional):
                    Defines the operation of node selection. Valid operators are IN for affinity and NOT_IN for anti-affinity.
                    Enum type. Allowed values:
                        "IN" - Requires Compute Engine to seek for matched nodes.
                        "NOT_IN" - Requires Compute Engine to avoid certain nodes.
                        "OPERATOR_UNSPECIFIED"

                * values (List[str], Optional):
                    Corresponds to the label values of Node resource.
                * key (str, Optional):
                    Corresponds to the label key of Node resource.

            * instance_termination_action (str, Optional):
                Specifies the termination action for the instance.
                Enum type. Allowed values:
                    "DELETE" - Delete the VM.
                    "INSTANCE_TERMINATION_ACTION_UNSPECIFIED" - Default value. This value is unused.
                    "STOP" - Stop the VM without storing in-memory content. default action.
            * provisioning_model (str, Optional):
                Specifies the provisioning model of the instance.
                Enum type. Allowed values:
                    "SPOT" - Heavily discounted, no guaranteed runtime.
                    "STANDARD" - Standard provisioning with user controlled runtime, no discounts.
            * location_hint (str, Optional):
                An opaque location hint used to place the instance close to other resources. This field is for use by internal tools that use the public API.

        private_ipv6_google_access(str, Optional):
            The private IPv6 google access type for the VM. If not specified, use INHERIT_FROM_SUBNETWORK as default.
            Enum type. Allowed values:
                "ENABLE_BIDIRECTIONAL_ACCESS_TO_GOOGLE" - Bidirectional private IPv6 access to/from Google services. If specified, the subnetwork who is attached to the instance's default network interface will be assigned an internal IPv6 prefix if it doesn't have before.
                "ENABLE_OUTBOUND_VM_ACCESS_TO_GOOGLE" - Outbound private IPv6 access from VMs in this subnet to Google services. If specified, the subnetwork who is attached to the instance's default network interface will be assigned an internal IPv6 prefix if it doesn't have before.
                "INHERIT_FROM_SUBNETWORK" - Each network interface inherits PrivateIpv6GoogleAccess from its subnetwork. Defaults to None.

        description(str, Optional):
            An optional description of this resource. Provide this property when you create the resource. Defaults to None.

        guest_accelerators(List[Dict[str, Any]], Optional):
            A list of the type and count of accelerator cards attached to the instance. Defaults to None.

            * accelerator_count (int, Optional):
                The number of the guest accelerator cards exposed to this instance.
            * accelerator_type (str, Optional):
                Full or partial URL of the accelerator type resource to attach to this instance. For example: projects/my-project/zones/us-central1-c/acceleratorTypes/nvidia-tesla-p100 If you are creating an instance template, specify only the accelerator name. See GPUs on Compute Engine for a full list of accelerator types.

        confidential_instance_config(Dict[str, Any], Optional):
            ConfidentialInstanceConfig: A set of Confidential Instance options. Defaults to None.

            * enable_confidential_compute (bool, Optional):
                Defines whether the instance should have confidential compute enabled.

        shielded_instance_config(Dict[str, Any], Optional):
            ShieldedInstanceConfig: A set of Shielded Instance options. Defaults to None.

            * enable_vtpm (bool, Optional):
                Defines whether the instance has the vTPM enabled. Enabled by default.
            * enable_secure_boot (bool, Optional):
                Defines whether the instance has Secure Boot enabled. Disabled by default.
            * enable_integrity_monitoring (bool, Optional):
                Defines whether the instance has integrity monitoring enabled. Enabled by default.

        source_machine_image_encryption_key(Dict[str, Any], Optional):
            Source machine image encryption key when creating an instance from a machine image. Defaults to None.

            * kms_key_service_account (str, Optional):
                The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. For example: "kmsKeyServiceAccount": "name@project_id.iam.gserviceaccount.com/"
            * sha256 (str, Optional):
                [Output only] The RFC 4648 base64 encoded SHA-256 hash of the customer-supplied encryption key that protects this resource.
            * rsa_encrypted_key (str, Optional):
                Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rsaEncryptedKey": "ieCx/NcW06PcT7Ep1X6LUTc/hLvUDYyzSZPPVCVPTVEohpeHASqC8uw5TzyO9U+Fka9JFH z0mBibXUInrC/jEk014kCK/NPjYgEMOyssZ4ZINPKxlUh2zn1bV+MCaTICrdmuSBTWlUUiFoD D6PYznLwh8ZNdaheCeZ8ewEXgFQ8V+sDroLaN3Xs3MDTXQEMMoNUXMCZEIpg9Vtp9x2oe==" The key must meet the following requirements before you can provide it to Compute Engine: 1. The key is wrapped using a RSA public key certificate provided by Google. 2. After being wrapped, the key must be encoded in RFC 4648 base64 encoding. Gets the RSA public key certificate provided by Google at: https://cloud-certs.storage.googleapis.com/google-cloud-csek-ingress.pem
            * kms_key_name (str, Optional):
                The name of the encryption key that is stored in Google Cloud KMS. For example: "kmsKeyName": "projects/kms_project_id/locations/region/keyRings/ key_region/cryptoKeys/key
            * raw_key (str, Optional):
                Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rawKey": "SGVsbG8gZnJvbSBHb29nbGUgQ2xvdWQgUGxhdGZvcm0="

        disks(List[Dict[str, Any]], Optional):
            Array of disks associated with this instance. Persistent disks must be created before you can assign them. Defaults to None.

            * disk_size_gb (str, Optional):
                The size of the disk in GB.
            * auto_delete (bool, Optional):
                Specifies whether the disk will be auto-deleted when the instance is deleted (but not when the disk is detached from the instance).
            * boot (bool, Optional):
                Indicates that this is a boot disk. The virtual machine will use the first partition of the disk for its root filesystem.
            * guest_os_features (List[Dict[str, Any]], Optional):
                A list of features to enable on the guest operating system. Applicable only for bootable images. Read Enabling guest operating system features to see a list of available options.

                * type (str, Optional):
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
            * source (str, Optional):
                Specifies a valid partial or full URL to an existing Persistent Disk resource. When creating a new instance, one of initializeParams.sourceImage or initializeParams.sourceSnapshot or disks.source is required except for local SSD. If desired, you can also attach existing non-root persistent disks using this property. This field is only applicable for persistent disks. Note that for InstanceTemplate, specify the disk name for zonal disk, and the URL for regional disk.
            * disk_encryption_key (Dict[str, Any], Optional):
                Encrypts or decrypts a disk using a customer-supplied encryption key. If you are creating a new disk, this field encrypts the new disk using an encryption key that you provide. If you are attaching an existing disk that is already encrypted, this field decrypts the disk using the customer-supplied encryption key. If you encrypt a disk using a customer-supplied key, you must provide the same key again when you attempt to use this resource at a later time. For example, you must provide the key when you create a snapshot or an image from the disk or when you attach the disk to a virtual machine instance. If you do not provide an encryption key, then the disk will be encrypted using an automatically generated key and you do not need to provide a key to use the disk later. Instance templates do not store customer-supplied encryption keys, so you cannot use your own keys to encrypt disks in a managed instance group.

                * kms_key_service_account (str, Optional):
                    The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. For example: "kmsKeyServiceAccount": "name@project_id.iam.gserviceaccount.com/"
                * sha256 (str, Optional):
                    [Output only] The RFC 4648 base64 encoded SHA-256 hash of the customer-supplied encryption key that protects this resource.
                * rsa_encrypted_key (str, Optional):
                    Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rsaEncryptedKey": "ieCx/NcW06PcT7Ep1X6LUTc/hLvUDYyzSZPPVCVPTVEohpeHASqC8uw5TzyO9U+Fka9JFH z0mBibXUInrC/jEk014kCK/NPjYgEMOyssZ4ZINPKxlUh2zn1bV+MCaTICrdmuSBTWlUUiFoD D6PYznLwh8ZNdaheCeZ8ewEXgFQ8V+sDroLaN3Xs3MDTXQEMMoNUXMCZEIpg9Vtp9x2oe==" The key must meet the following requirements before you can provide it to Compute Engine: 1. The key is wrapped using a RSA public key certificate provided by Google. 2. After being wrapped, the key must be encoded in RFC 4648 base64 encoding. Gets the RSA public key certificate provided by Google at: https://cloud-certs.storage.googleapis.com/google-cloud-csek-ingress.pem
                * kms_key_name (str, Optional):
                    The name of the encryption key that is stored in Google Cloud KMS. For example: "kmsKeyName": "projects/kms_project_id/locations/region/keyRings/ key_region/cryptoKeys/key
                * raw_key (str, Optional):
                    Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rawKey": "SGVsbG8gZnJvbSBHb29nbGUgQ2xvdWQgUGxhdGZvcm0="
            * force_attach (bool, Optional):
                [Input Only] Whether to force attach the regional disk even if it's currently attached to another instance. If you try to force attach a zonal disk to an instance, you will receive an error.
            * architecture (str, Optional):
                [Output Only] The architecture of the attached disk. Valid values are ARM64 or X86_64.
                Enum type. Allowed values:
                    "ARCHITECTURE_UNSPECIFIED" - Default value indicating Architecture is not set.
                    "ARM64" - Machines with architecture ARM64
                    "X86_64" - Machines with architecture X86_64
            * device_name (str, Optional):
                Specifies a unique device name of your choice that is reflected into the /dev/disk/by-id/google-* tree of a Linux operating system running within the instance. This name can be used to reference the device for mounting, resizing, and so on, from within the instance. If not specified, the server chooses a default device name to apply to this disk, in the form persistent-disk-x, where x is a number assigned by Google Compute Engine. This field is only applicable for persistent disks.
            * shielded_instance_initial_state (Dict[str, Any], Optional):
                [Output Only] shielded vm initial state stored on disk.
                InitialStateConfig: Initial State for shielded instance, these are public keys which are safe to store in public

                * keks (List[Dict[str, Any]], Optional):
                    The Key Exchange Key (KEK).

                    * file_type (str, Optional):
                        The file type of source file.
                        Enum type. Allowed values:
                            "BIN"
                            "UNDEFINED"
                            "X509"
                    * content (str, Optional):
                        The raw content in the secure keys file.
                * dbs (List[Dict[str, Any]], Optional):
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
            * initialize_params (Dict[str, Any], Optional):
                [Input Only] Specifies the parameters for a new disk that will be created alongside the new instance. Use initialization parameters to create boot disks or local SSDs attached to the new instance. This property is mutually exclusive with the source property; you can only define one or the other, but not both.
                AttachedDiskInitializeParams: [Input Only] Specifies the parameters for a new disk that will be created alongside the new instance. Use initialization parameters to create boot disks or local SSDs attached to the new instance. This field is persisted and returned for instanceTemplate and not returned in the context of instance. This property is mutually exclusive with the source property; you can only define one or the other, but not both.

                * resource_manager_tags (Dict[str, Any], Optional):
                    Resource manager tags to be bound to the disk. Tag keys and values have the same definition as resource manager tags. Keys must be in the format `tagKeys/{tag_key_id}`, and values are in the format `tagValues/456`. The field is ignored (both PUT & PATCH) when empty.
                * source_image (str, Optional):
                    The source image to create this disk. When creating a new instance, one of initializeParams.sourceImage or initializeParams.sourceSnapshot or disks.source is required except for local SSD. To create a disk with one of the public operating system images, specify the image by its family name. For example, specify family/debian-9 to use the latest Debian 9 image: projects/debian-cloud/global/images/family/debian-9 Alternatively, use a specific version of a public operating system image: projects/debian-cloud/global/images/debian-9-stretch-vYYYYMMDD To create a disk with a custom image that you created, specify the image name in the following format: global/images/my-custom-image You can also specify a custom image by its image family, which returns the latest version of the image in that family. Replace the image name with family/family-name: global/images/family/my-image-family If the source image is deleted later, this field will not be set.
                * description (str, Optional):
                    An optional description. Provide this property when creating the disk.
                * disk_size_gb (str, Optional):
                    Specifies the size of the disk in base-2 GB. The size must be at least 10 GB. If you specify a sourceImage, which is required for boot disks, the default size is the size of the sourceImage. If you do not specify a sourceImage, the default disk size is 500 GB.
                * source_snapshot (str, Optional):
                    The source snapshot to create this disk. When creating a new instance, one of initializeParams.sourceSnapshot or initializeParams.sourceImage or disks.source is required except for local SSD. To create a disk with a snapshot that you created, specify the snapshot name in the following format: global/snapshots/my-backup If the source snapshot is deleted later, this field will not be set.
                * provisioned_iops (str, Optional):
                    Indicates how many IOPS to provision for the disk. This sets the number of I/O operations per second that the disk can handle. Values must be between 10,000 and 120,000. For more details, see the Extreme persistent disk documentation.
                * source_image_encryption_key (Dict[str, Any], Optional):
                    The customer-supplied encryption key of the source image. Required if the source image is protected by a customer-supplied encryption key. InstanceTemplate and InstancePropertiesPatch do not store customer-supplied encryption keys, so you cannot create disks for instances in a managed instance group if the source images are encrypted with your own keys.

                    * kms_key_service_account (str, Optional):
                        The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. For example: "kmsKeyServiceAccount": "name@project_id.iam.gserviceaccount.com/"
                    * sha256 (str, Optional):
                        [Output only] The RFC 4648 base64 encoded SHA-256 hash of the customer-supplied encryption key that protects this resource.
                    * rsa_encrypted_key (str, Optional):
                        Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rsaEncryptedKey": "ieCx/NcW06PcT7Ep1X6LUTc/hLvUDYyzSZPPVCVPTVEohpeHASqC8uw5TzyO9U+Fka9JFH z0mBibXUInrC/jEk014kCK/NPjYgEMOyssZ4ZINPKxlUh2zn1bV+MCaTICrdmuSBTWlUUiFoD D6PYznLwh8ZNdaheCeZ8ewEXgFQ8V+sDroLaN3Xs3MDTXQEMMoNUXMCZEIpg9Vtp9x2oe==" The key must meet the following requirements before you can provide it to Compute Engine: 1. The key is wrapped using a RSA public key certificate provided by Google. 2. After being wrapped, the key must be encoded in RFC 4648 base64 encoding. Gets the RSA public key certificate provided by Google at: https://cloud-certs.storage.googleapis.com/google-cloud-csek-ingress.pem
                    * kms_key_name (str, Optional):
                        The name of the encryption key that is stored in Google Cloud KMS. For example: "kmsKeyName": "projects/kms_project_id/locations/region/keyRings/ key_region/cryptoKeys/key
                    * raw_key (str, Optional):
                        Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rawKey": "SGVsbG8gZnJvbSBHb29nbGUgQ2xvdWQgUGxhdGZvcm0="
                * on_update_action (str, Optional):
                    Specifies which action to take on instance update with this disk. Default is to use the existing disk.
                    Enum type. Allowed values:
                        "RECREATE_DISK" - Always recreate the disk.
                        "RECREATE_DISK_IF_SOURCE_CHANGED" - Recreate the disk if source (image, snapshot) of this disk is different from source of existing disk.
                        "USE_EXISTING_DISK" - Use the existing disk, this is the default behaviour.
                * source_snapshot_encryption_key (Dict[str, Any], Optional):
                    The customer-supplied encryption key of the source snapshot.

                    * kms_key_service_account (str, Optional):
                        The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. For example: "kmsKeyServiceAccount": "name@project_id.iam.gserviceaccount.com/"
                    * sha256 (str, Optional):
                        [Output only] The RFC 4648 base64 encoded SHA-256 hash of the customer-supplied encryption key that protects this resource.
                    * rsa_encrypted_key (str, Optional):
                        Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rsaEncryptedKey": "ieCx/NcW06PcT7Ep1X6LUTc/hLvUDYyzSZPPVCVPTVEohpeHASqC8uw5TzyO9U+Fka9JFH z0mBibXUInrC/jEk014kCK/NPjYgEMOyssZ4ZINPKxlUh2zn1bV+MCaTICrdmuSBTWlUUiFoD D6PYznLwh8ZNdaheCeZ8ewEXgFQ8V+sDroLaN3Xs3MDTXQEMMoNUXMCZEIpg9Vtp9x2oe==" The key must meet the following requirements before you can provide it to Compute Engine: 1. The key is wrapped using a RSA public key certificate provided by Google. 2. After being wrapped, the key must be encoded in RFC 4648 base64 encoding. Gets the RSA public key certificate provided by Google at: https://cloud-certs.storage.googleapis.com/google-cloud-csek-ingress.pem
                    * kms_key_name (str, Optional):
                        The name of the encryption key that is stored in Google Cloud KMS. For example: "kmsKeyName": "projects/kms_project_id/locations/region/keyRings/ key_region/cryptoKeys/key
                    * raw_key (str, Optional):
                        Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. For example: "rawKey": "SGVsbG8gZnJvbSBHb29nbGUgQ2xvdWQgUGxhdGZvcm0="

                * architecture (str, Optional):
                    The architecture of the attached disk. Valid values are arm64 or x86_64.
                    Enum type. Allowed values:
                        "ARCHITECTURE_UNSPECIFIED" - Default value indicating Architecture is not set.
                        "ARM64" - Machines with architecture ARM64
                        "X86_64" - Machines with architecture X86_64
                * licenses (List[str], Optional):
                    A list of publicly visible licenses. Reserved for Google's use.
                * labels (Dict[str, Any], Optional):
                    Labels to apply to this disk. These can be later modified by the disks.setLabels method. This field is only applicable for persistent disks.
                * disk_type (str, Optional):
                    Specifies the disk type to use to create the instance. If not specified, the default is pd-standard, specified using the full URL. For example: https://www.googleapis.com/compute/v1/projects/project/zones/zone/diskTypes/pd-standard For a full list of acceptable values, see Persistent disk types. If you specify this field when creating a VM, you can provide either the full or partial URL. For example, the following values are valid: - https://www.googleapis.com/compute/v1/projects/project/zones/zone /diskTypes/diskType - projects/project/zones/zone/diskTypes/diskType - zones/zone/diskTypes/diskType If you specify this field when creating or updating an instance template or all-instances configuration, specify the type of the disk, not the URL. For example: pd-standard.
                * disk_name (str, Optional):
                    Specifies the disk name. If not specified, the default is to use the name of the instance. If a disk with the same name already exists in the given region, the existing disk is attached to the new instance and the new disk is not created.
                * resource_policies (List[str], Optional):
                    Resource policies applied to this disk for automatic snapshot creations. Specified using the full or partial URL. For instance template, specify only the resource policy name.

            * kind (str, Optional):
                [Output Only] Type of the resource. Always compute#attachedDisk for attached disks.
            * index (int, Optional):
                [Output Only] A zero-based index to this disk, where 0 is reserved for the boot disk. If you have many disks attached to an instance, each disk would have a unique index number.
            * interface (str, Optional):
                Specifies the disk interface to use for attaching this disk, which is either SCSI or NVME. For most machine types, the default is SCSI. Local SSDs can use either NVME or SCSI. In certain configurations, persistent disks can use NVMe. For more information, see About persistent disks.
                Enum type. Allowed values:
                    "NVME"
                    "SCSI"
            * licenses (List[str], Optional):
                [Output Only] Any valid publicly visible licenses.
            * mode (str, Optional):
                The mode in which to attach this disk, either READ_WRITE or READ_ONLY. If not specified, the default is to attach the disk in READ_WRITE mode.
                Enum type. Allowed values:
                    "READ_ONLY" - Attaches this disk in read-only mode. Multiple virtual machines can use a disk in read-only mode at a time.
                    "READ_WRITE" - *[Default]* Attaches this disk in read-write mode. Only one virtual machine at a time can be attached to a disk in read-write mode.
            * type (str, Optional):
                Specifies the type of the disk, either SCRATCH or PERSISTENT. If not specified, the default is PERSISTENT.
                Enum type. Allowed values:
                    "PERSISTENT"
                    "SCRATCH"

        hostname(str, Optional):
            Specifies the hostname of the instance. The specified hostname must be RFC1035 compliant. If hostname is not specified, the default hostname is [INSTANCE_NAME].c.[PROJECT_ID].internal when using the global DNS, and [INSTANCE_NAME].[ZONE].c.[PROJECT_ID].internal when using zonal DNS. Defaults to None.

        network_performance_config(Dict[str, Any], Optional):
            Defaults to None.

            * total_egress_bandwidth_tier (str, Optional):
                Enum type. Allowed values:
                    "DEFAULT"
                    "TIER_1"

        params(Dict[str, Any], Optional):
            Input only. [Input Only] Additional params passed with the request, but not persisted as part of resource payload.
            InstanceParams: Additional instance params. Defaults to None.

            * resource_manager_tags (Dict[str, Any], Optional):
                Resource manager tags to be bound to the instance. Tag keys and values have the same definition as resource manager tags. Keys must be in the format `tagKeys/{tag_key_id}`, and values are in the format `tagValues/456`. The field is ignored (both PUT & PATCH) when empty.

                ResourceStatus: Contains output only fields. Use this sub-message for actual values set on Instance attributes as compared to the value requested by the user (intent) in their instance CRUD calls. Defaults to None.
            * physical_host (str, Optional):
                [Output Only] An opaque ID of the host on which the VM is running.

        deletion_protection(bool, Optional):
            Whether the resource should be protected against deletion. Defaults to None.

        metadata(Dict[str, Any], Optional):
            The metadata key/value pairs assigned to this instance. This includes custom metadata and predefined keys.
            Metadata: A metadata key/value entry. Defaults to None.

            * items (List[Dict[str, Any]], Optional):
                Array of key/value pairs. The total size of all keys and values must be less than 512 KB.

                * key (str, Optional):
                    Key for the metadata entry. Keys must conform to the following regexp: [a-zA-Z0-9-_]+, and be less than 128 bytes in length. This is reflected as part of a URL in the metadata server. Additionally, to avoid ambiguity, keys must not conflict with any other metadata keys for the project.
                * value (str, Optional):
                    Value for the metadata entry. These are free-form strings, and only have meaning as interpreted by the image running in the instance. The only restriction placed on values is that their size must be less than or equal to 262144 bytes (256 KiB).

            * kind (str, Optional):
                [Output Only] Type of the resource. Always compute#metadata for metadata.
            * fingerprint (str, Optional):
                Specifies a fingerprint for this request, which is essentially a hash of the metadata's contents and used for optimistic locking. The fingerprint is initially generated by Compute Engine and changes after every request to modify or update metadata. You must always provide an up-to-date fingerprint hash in order to update or change metadata, otherwise the request will fail with error 412 conditionNotMet. To see the latest fingerprint, make a get() request to retrieve the resource.

        zone(str):
            The name of the zone for this request.

        shielded_instance_integrity_policy(Dict[str, Any], Optional):
            ShieldedInstanceIntegrityPolicy: The policy describes the baseline against which Instance boot integrity is measured. Defaults to None.

            * update_auto_learn_policy (bool, Optional):
                Updates the integrity policy baseline using the measurements from the VM instance's most recent boot.

        reservation_affinity(Dict[str, Any], Optional):
            Specifies the reservations that this instance can consume from.
            ReservationAffinity: Specifies the reservations that this instance can consume from. Defaults to None.

            * key (str, Optional):
                Corresponds to the label key of a reservation resource. To target a SPECIFIC_RESERVATION by name, specify googleapis.com/reservation-name as the key and specify the name of your reservation as its value.
            * values (List[str], Optional):
                Corresponds to the label values of a reservation resource. This can be either a name to a reservation in the same project or "projects/different-project/reservations/some-reservation-name" to target a shared reservation in the same zone but in a different project.
            * consume_reservation_type (str, Optional):
                Specifies the type of reservation from which this instance can consume resources: ANY_RESERVATION (default), SPECIFIC_RESERVATION, or NO_RESERVATION. See Consuming reserved instances for examples.
                Enum type. Allowed values:
                    "ANY_RESERVATION" - Consume any allocation available.
                    "NO_RESERVATION" - Do not consume from any allocated capacity.
                    "SPECIFIC_RESERVATION" - Must consume from a specific reservation. Must specify key value fields for specifying the reservations.
                    "UNSPECIFIED"

        min_cpu_platform(str, Optional):
            Specifies a minimum CPU platform for the VM instance. Applicable values are the friendly names of CPU platforms, such as minCpuPlatform: "Intel Haswell" or minCpuPlatform: "Intel Sandy Bridge". Defaults to None.

        machine_type(str, Optional):
            Full or partial URL of the machine type resource to use for this instance, in the format: zones/zone/machineTypes/machine-type. This is provided by the client when the instance is created. For example, the following is a valid partial url to a predefined machine type: zones/us-central1-f/machineTypes/n1-standard-1 To create a custom machine type, provide a URL to a machine type in the following format, where CPUS is 1 or an even number up to 32 (2, 4, 6, ... 24, etc), and MEMORY is the total memory for this instance. Memory must be a multiple of 256 MB and must be supplied in MB (e.g. 5 GB of memory is 5120 MB): zones/zone/machineTypes/custom-CPUS-MEMORY For example: zones/us-central1-f/machineTypes/custom-4-5120 For a full list of restrictions, read the Specifications for custom machine types. Defaults to None.

        project(str, Optional):
            Project ID for this request.

        source_instance_template(str, Optional):
            Specifies instance template to create the instance. This field is optional. It can be a full or partial URL. For example, the following are all valid URLs to an instance template:

            - https://www.googleapis.com/compute/v1/projects/project/global/instanceTemplates/instanceTemplate
            - projects/project/global/instanceTemplates/instanceTemplate
            - global/instanceTemplates/instanceTemplate

            Defaults to None.

        source_machine_image(str, Optional):
            Specifies the machine image to use to create the instance. This field is optional. It can be a full or partial URL. Defaults to None. For example, the following are all valid URLs to a machine image. Defaults to None.:

            - https://www.googleapis.com/compute/v1/projects/project/global/global/machineImages/machineImage
            - projects/project/global/global/machineImages/machineImage
            - global/machineImages/machineImage

        request_id(str, Optional):
            An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

        minimal_action(str, Optional):
            Specifies the action to take when updating an instance even if the updated properties do not require it. If not specified, then Compute Engine acts based on the minimum action that the updated properties require. Defaults to None.

        most_disruptive_allowed_action(str, Optional):
            Specifies the most disruptive action that can be taken on the instance as part of the update. Compute Engine returns an error if the instance properties require a more disruptive action as part of the instance update. Valid options from lowest to highest are NO_EFFECT, REFRESH, and RESTART. Defaults to None.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        id(str, Optional):
            The unique identifier for the resource. This identifier is defined by the server. Read-only property

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            example-resource-name:
              gcp.compute.instance.present:
              - project: example-project
              - machine_type: https://www.googleapis.com/compute/v1/projects/example-project/zones/us-central1-a/machineTypes/g1-small
              - zone: us-central1-a
              - can_ip_forward: false
              - network_interfaces:
                - access_configs:
                  - kind: compute#accessConfig
                    name: External NAT
                    network_tier: PREMIUM
                    set_public_ptr: false
                    type_: ONE_TO_ONE_NAT
                  kind: compute#networkInterface
                  name: nic0
                  network: https://www.googleapis.com/compute/v1/projects/project-name/global/networks/default
                  stack_type: IPV4_ONLY
                  subnetwork: https://www.googleapis.com/compute/v1/projects/project-name/regions/us-central1/subnetworks/default
              - disks:
                - auto_delete: true
                  boot: true
                  device_name: example_disk_1
                  source: https://www.googleapis.com/compute/v1/projects/project-name/zones/us-central1-a/disks/example_disk_1
                  mode: READ_WRITE
                  type_: PERSISTENT
                  disk_size_gb: '10'
                  index: 0
                  interface: SCSI
                  kind: compute#attachedDisk
              - scheduling:
                  automatic_restart: true
                  on_host_maintenance: MIGRATE
                  preemptible: false
                  provisioning_model: STANDARD
              - deletion_protection: false
              - tags:
                  items:
                    - test
              - metadata:
                  kind: compute#metadata
                  items:
                    - key: sample_metadata_key
                      value: sample_metadata_value
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

    # to be autogenerated by pop-create based on insert/update props in properties.yaml
    resource_body = {
        "service_accounts": service_accounts,
        "name": name,
        "min_cpu_platform": min_cpu_platform,
        "disks": disks,
        "network_performance_config": network_performance_config,
        "shielded_instance_integrity_policy": shielded_instance_integrity_policy,
        "private_ipv6_google_access": private_ipv6_google_access,
        "source_machine_image_encryption_key": source_machine_image_encryption_key,
        "confidential_instance_config": confidential_instance_config,
        "guest_accelerators": guest_accelerators,
        "description": description,
        "metadata": metadata,
        "resource_policies": resource_policies,
        "key_revocation_action_type": key_revocation_action_type,
        "hostname": hostname,
        "reservation_affinity": reservation_affinity,
        "tags": tags,
        "scheduling": scheduling,
        "advanced_machine_features": advanced_machine_features,
        "params": params,
        "machine_type": machine_type,
        "source_machine_image": source_machine_image,
        "shielded_instance_config": shielded_instance_config,
        "labels": labels,
        "deletion_protection": deletion_protection,
        "network_interfaces": network_interfaces,
        "can_ip_forward": can_ip_forward,
        "display_device": display_device,
        "zone": zone,
        "status": status,
        "id_": id_,
    }

    resource_body = {k: v for (k, v) in resource_body.items() if v is not None}
    operation = None
    if result["old_state"]:
        resource_id = result["old_state"].get("resource_id", None)
        zone = hub.tool.gcp.resource_prop_utils.parse_link_to_zone(
            result["old_state"]["zone"]
        )
        result["old_state"]["zone"] = zone

        # The fingerprint is required upon an update operation but in the time of creation the
        # resource still do not have fingerprint so, we cannot make it a required param for present method.
        resource_body["fingerprint"] = fingerprint or result["old_state"].get(
            "fingerprint"
        )
        resource_body["label_fingerprint"] = label_fingerprint or result[
            "old_state"
        ].get("label_fingerprint")

        # A dictionary of additional operations to perform on the object identified by the key
        # the values are tuples with the first element - the method to call, the second element - arguments,
        # third - the property is required in the end result
        patch_operations_dict = {
            "network_interfaces": (
                hub.tool.gcp.compute.instance.update_network_interfaces,
                (ctx, result["old_state"], network_interfaces),
                True,
            ),
            "status": (
                hub.tool.gcp.compute.instance.update_status,
                (ctx, resource_id, result["old_state"].get("status"), status),
                True,
            ),
            "shielded_instance_config": (
                hub.tool.gcp.compute.instance.update_shielded_instance_config,
                (ctx, shielded_instance_config, None, None, None, resource_id),
                False,
            ),
            "shielded_instance_integrity_policy": (
                hub.tool.gcp.compute.instance.update_shielded_instance_integrity_policy,
                (
                    ctx,
                    shielded_instance_integrity_policy,
                    None,
                    None,
                    None,
                    resource_id,
                ),
                False,
            ),
        }

        state_operations = StateOperations(
            hub, "compute.instance", patch_operations_dict, result, resource_body
        )

        changes = hub.tool.gcp.utils.compare_states(
            result["old_state"],
            {
                "resource_id": resource_id,
                **resource_body,
            },
            "compute.instance",
            additional_exclude_paths=list(patch_operations_dict.keys()),
        )

        if changes:
            changed_non_updatable_properties = (
                hub.tool.gcp.resource_prop_utils.get_changed_non_updatable_properties(
                    "compute.instance", changes
                )
            )
            if changed_non_updatable_properties:
                result["result"] = False
                result["comment"].append(
                    hub.tool.gcp.comment_utils.non_updatable_properties_comment(
                        "gcp.compute.instance",
                        name,
                        changed_non_updatable_properties,
                    )
                )
                result["new_state"] = result["old_state"]
                return result

        if not changes and not any(state_operations.changed_properties_dict.values()):
            result["result"] = True
            result["comment"].append(
                hub.tool.gcp.comment_utils.up_to_date_comment(
                    "gcp.compute.instance", name
                )
            )
            result["new_state"] = result["old_state"]
            return result

        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_update_comment(
                    "gcp.compute.instance", name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                resource_body
            )
            result["new_state"]["resource_id"] = resource_id
            return result

        state_operations_ret = await state_operations.run_operations()

        current_state = result["old_state"]
        if "new_state" in state_operations_ret:
            current_state = state_operations_ret["new_state"]
        elif any(state_operations.changed_properties_dict.values()):
            get_ret = await hub.exec.gcp.compute.instance.get(
                ctx, resource_id=resource_id
            )
            if not get_ret["result"] or not get_ret["ret"]:
                result["result"] = False
                result["comment"] += get_ret["comment"]
                return result
            current_state = get_ret["ret"]
        result["new_state"] = current_state

        if not state_operations_ret["result"]:
            result["comment"] += state_operations_ret["comment"]
            result["result"] = False
            return result

        if changes:
            if any(state_operations.changed_properties_dict.values()):
                for k in patch_operations_dict.keys():
                    resource_body[k] = current_state.get(k)

                resource_body["fingerprint"] = current_state.get("fingerprint")
                resource_body["label_fingerprint"] = current_state.get(
                    "label_fingerprint"
                )

            state_operations.pre_process_resource_body(resource_body)

            update_ret = await hub.exec.gcp_api.client.compute.instance.update(
                hub,
                ctx,
                name=name,
                resource_id=resource_id,
                minimal_action=minimal_action,
                most_disruptive_allowed_action=most_disruptive_allowed_action,
                body=resource_body,
            )

            if not update_ret["result"] or not update_ret["ret"]:
                result["result"] = False
                result["comment"] += update_ret["comment"]
                return result

            if hub.tool.gcp.operation_utils.is_operation(update_ret["ret"]):
                operation = update_ret["ret"]

        if not changes and any(state_operations.changed_properties_dict.values()):
            get_ret = await hub.exec.gcp.compute.instance.get(
                ctx, resource_id=resource_id
            )
            if not get_ret["result"] and not get_ret["ret"]:
                result["result"] = False
                result["comment"] += get_ret["comment"]
                return result

            result["new_state"] = get_ret["ret"]
            result["comment"].append(
                hub.tool.gcp.comment_utils.update_comment("gcp.compute.instance", name)
            )
            return result

    else:
        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    "gcp.compute.instance", name
                )
            )
            result["new_state"] = hub.tool.gcp.sanitizers.sanitize_resource_urls(
                resource_body
            )
            result["new_state"]["resource_id"] = resource_id
            return result

        # Create
        create_ret = await hub.exec.gcp_api.client.compute.instance.insert(
            ctx,
            name=name,
            project=project,
            zone=zone,
            source_instance_template=source_instance_template,
            request_id=request_id,
            body=resource_body,
        )
        if not create_ret["result"] or not create_ret["ret"]:
            result["result"] = False
            if create_ret["comment"] and next(
                (
                    comment
                    for comment in create_ret["comment"]
                    if "alreadyExists" in comment
                ),
                None,
            ):
                result["comment"].append(
                    hub.tool.gcp.comment_utils.already_exists_comment(
                        "gcp.compute.instance", name
                    )
                )
            else:
                result["comment"] += create_ret["comment"]
            return result

        if hub.tool.gcp.operation_utils.is_operation(create_ret["ret"]):
            operation = create_ret["ret"]

    if operation:
        operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            operation.get("selfLink"), "compute.zone_operation"
        )
        result["rerun_data"] = {
            "operation_id": operation_id,
            "old_state": result["old_state"],
            "on_completion": {
                "handler": "hub.tool.gcp.compute.instance.on_completion",
                "aux_ctx": {"status": status},
            },
        }
        return result

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Retrieves the list of instances contained within the specified zone.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe gcp.compute.instance

    """
    result = {}

    describe_ret = await hub.exec.gcp.compute.instance.list(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(f"Could not describe instances {describe_ret['comment']}")
        return {}

    for resource in describe_ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "gcp.compute.instance.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.gcp.utils.is_pending(ret=ret, state=state, **pending_kwargs)
