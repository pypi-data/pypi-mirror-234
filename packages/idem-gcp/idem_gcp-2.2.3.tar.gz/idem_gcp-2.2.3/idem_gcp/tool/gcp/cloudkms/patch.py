from typing import Any
from typing import Dict

import deepdiff
from dict_tools.data import NamespaceDict


def calc_update_mask(hub, sls_data: Dict[str, Any], gcp_data: Dict[str, Any]) -> str:
    """Calculate update mask needed for patch methods in cloudkms.

    Do not include in the update mask properties present only in gcp_data.

    Args:
        sls_data: First object to diff.
        gcp_data: Second object to diff

    Returns:
         List of fields to be updated in this request. None if there are no differences.

         This is a comma-separated list of fully qualified names of fields. Example: "user.displayName,photo".
    """
    if (
        type(sls_data) != type(gcp_data)
        and type(sls_data) not in (NamespaceDict, dict)
        and type(gcp_data) not in (NamespaceDict, dict)
    ):
        raise Exception(
            f"Dictionary params are of different types ({type(sls_data)} - {type(gcp_data)}."
            " deepdiff will not work correctly"
        )
    diff = deepdiff.DeepDiff(
        sls_data,
        gcp_data,
        ignore_order=True,
        view="tree",
        ignore_type_in_groups=[(NamespaceDict, dict)],
    )

    paths = set()
    for k in diff.affected_paths:
        if (
            isinstance(k.t1, deepdiff.helper.NotPresent)
            and not k.get_root_key() == "labels"
        ):
            continue
        p = k.path(output_format="list")
        # ["labels", "label_key"]
        root_key = k.get_root_key()
        if root_key == "labels":
            paths.add(root_key)
        else:
            paths.add(".".join(p))

    return ",".join(paths) if len(paths) > 0 else None


def merge_labels(
    hub, new_labels: Dict[str, str], old_labels: Dict[str, str]
) -> Dict[str, str]:
    if new_labels is None:
        return old_labels or {}
    elif old_labels is None:
        return new_labels

    return {**old_labels, **new_labels}
