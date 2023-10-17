"""GCP init module."""


def __init__(hub):
    # This enables acct profiles that begin with "gcp" for states
    hub.states.gcp.ACCT = ["gcp"]
