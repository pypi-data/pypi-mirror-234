from typing import List


def are_lists_identical(hub, list1: List, list2: List) -> bool:
    if not list1 and not list2:
        return True
    if list1 is None or len(list1) == 0 or list2 is None or len(list2) == 0:
        return False

    for l in [list1, list2]:
        if not isinstance(l, List):
            raise TypeError(
                f"Expecting lists to compare. This is expected to be of type List: '{l}'"
            )

    diff = [i for i in list1 + list2 if i not in list1 or i not in list2]
    result = len(diff) == 0
    if not result:
        hub.log.debug(f"There are {len(diff)} differences.")
    return result
