"""Google API Python client library exec module.

Copyright (c) 2021-2022 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0

This file implements the entirety of the Plugin Oriented Programming (POP)
exec Sub for Google discovery-based Python client library APIs.

The basic operating model is building Subs as needed to match the nature of a
call to an exec. For example, a call like:

    hub.exec.gcp_api.client.compute.instance.get(ctx, ...)

will work, even though no exec subdirectories exist to match that call path.
Instead, the API is dynamically discovered and built to match and tie
them to the appropriate GCP Python SDK wrappers within the tool Sub of this
project.
"""


def __init__(hub):
    """Initializes this module.

    :param hub: The Hub in which this Sub exists.
    """
    hub.exec.gcp_api.ACCT = ["gcp"]
    # hub.exec.gcp.OBJECT_CACHE = _GCP_SUB_CACHE
    hub.pop.sub.dynamic(
        sub=hub.exec.gcp_api,
        subname="client",
        resolver=hub.tool.gcp.resolver.resolve_sub,
        context=hub.tool.gcp.API,
    )
