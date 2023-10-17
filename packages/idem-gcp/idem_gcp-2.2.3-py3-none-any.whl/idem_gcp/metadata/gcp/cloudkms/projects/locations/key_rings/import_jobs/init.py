"""Metadata module for managing Crypto Key."""


def __init__(hub):
    hub.metadata.gcp.cloudkms.projects.locations.key_rings.import_jobs.PATH = "projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/importJobs/{import_job_id}"
