"""Google Cloud Platform provider exceptions module.

Copyright (c) 2021 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""
from functools import wraps


def entry_exit_log(func):
    """Decorator function to log function/method entry and exits.

    :param func: The function to decorate.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Logs any entry and exit to the wrapped func.

        :param args: All positional args to func.
        :param kwargs: All keyword args to the func.
        """
        func_fqn = f"{func.__module__}.{func.__name__}"
        hub = args[0]
        hub.log.debug(f"Entering {func_fqn}")
        r = func(*args, **kwargs)
        hub.log.debug(f"Exiting {func_fqn}")
        return r

    return wrapper
