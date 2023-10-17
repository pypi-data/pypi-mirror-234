from typing import Any
from typing import Dict


class StateOperations:
    r"""Helper class for additional 'PATCH/UPDATE' operations that are executed during handling of present method
    to update properties the generic patch/methods don't handle
    """

    def __init__(
        self,
        hub,
        resource_type: str,
        patch_operations_dict: Dict[str, Any],
        result: Dict[str, Any],
        resource_body: Dict[str, Any],
    ):
        r"""
        Args:
            patch_operations_dict(Dict[str, Any]):
                A dictionary of additional operations to perform on the object identified by the key.
                The values are tuples with the first element - the method to call, the second element - arguments, third - the property is required in the end result
                fourth - should the property be removed from the request_body(some patch operations complain)
        """
        self.resource_type = resource_type
        self.patch_operations_dict = patch_operations_dict
        self.old_properties_dict = {
            k: result["old_state"].get(k)
            for k in patch_operations_dict.keys()
            if result["old_state"].get(k) is not None
        }
        self.changed_properties_dict = {
            k: {}
            if resource_body.get(k) is None
            else hub.tool.gcp.utils.compare_states(
                {k: self.old_properties_dict.get(k)},
                {k: resource_body.get(k)},
                resource_type,
            )
            for k in patch_operations_dict.keys()
        }

    async def run_operations(self) -> Dict[str, Any]:
        ret = None
        r"""run all relevant(updated) operations"""
        for k, op in self.patch_operations_dict.items():
            if self.changed_properties_dict[k]:
                ret = await op[0](*op[1])

                if not ret["result"]:
                    return {"result": False, "comment": ret["comment"]}

        return (
            {"result": True, "new_state": ret["ret"]}
            if ret and "ret" in ret
            else {"result": True}
        )

    def pre_process_resource_body(self, resource_body: Dict[str, Any]):
        r"""puts back the old properties in the resource body so that the API doesn't complain"""
        for k, v in self.patch_operations_dict.items():
            if 2 in v and v[2] and not resource_body.get(k):
                resource_body[k] = self.old_properties_dict[k]
            if 3 in v and v[3] and k in resource_body:
                resource_body.pop(k)
