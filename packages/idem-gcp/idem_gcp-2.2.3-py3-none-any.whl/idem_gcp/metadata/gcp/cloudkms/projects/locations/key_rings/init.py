"""Metadata module for managing Key Rings."""


def __init__(hub):
    hub.metadata.gcp.cloudkms.projects.locations.key_rings.PATH = (
        "projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}"
    )
