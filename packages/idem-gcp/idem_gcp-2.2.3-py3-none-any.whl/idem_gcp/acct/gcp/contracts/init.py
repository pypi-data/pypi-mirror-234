# VMware Idem Plugin
# Copyright (c) 2020-2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
from typing import Any
from typing import Dict

from google.auth.credentials import Credentials


def post_gather(hub, ctx) -> Dict[str, Any]:
    """
    Validate the return from a "gather" function
    """
    for profile, profile_ctx in ctx.ret.items():
        error_msg = f"{ctx.ref} profile formatted incorrectly: {profile}"
        assert "credentials" in profile_ctx, error_msg
        assert isinstance(profile_ctx["credentials"], Credentials), error_msg

    return ctx.ret
