"""BCP Resource Manager (AzureRM) exec contracts.

Copyright (c) 2021 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""


async def call(hub, ctx):
    """Override the default call contract in order to prevent Exception usurping by Idem.

    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values  for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    """
    return await ctx.func(*ctx.args, **ctx.kwargs)
