"""Google Cloud Platform provider exceptions module.

Copyright (c) 2021 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""


class StateReturn(dict):
    """Convenience class to manage POP state returns."""

    def __init__(self, name=None, result=None, comment=None, old_obj={}, new_obj={}):
        """Initialize an object of this class.

        :param name: The name of the state (e.g. from a SLS file).
        :param result: True if the state call works, False otherwise.
        :param comment: Any relevant comments to the state execution.
        For example a 200 code from an HTTP call or a mere readable comment.
        In some cases, users of StateReturn may also store additional 'comment'
        type material, such as Operations for use in future checks on the state
        of the operation.
        :param old_obj: For state changes, the object's state
        (e.g., dict of values).
        prior to any state change request executions.
        :param new_obj: For state changes, the new object's state after any
        state change equest executions.
        """
        super().__init__(
            [("name", name), ("result", result), ("comment", comment), ("changes", {})]
        )
        self["changes"] = {"old": old_obj if old_obj else {}, "new": new_obj}
