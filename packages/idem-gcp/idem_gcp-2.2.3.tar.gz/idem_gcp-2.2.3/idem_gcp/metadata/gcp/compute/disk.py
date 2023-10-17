"""Metadata module for managing Disks."""

PATH = [
    "projects/{project}/zones/{zone}/disks/{disk}",
    "projects/{project}/regions/{region}/disks/{disk}",
]

NATIVE_RESOURCE_TYPE = [
    "compute.disks",
    "compute.regionDisks",
]
