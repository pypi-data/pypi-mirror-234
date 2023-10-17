from inspect import signature

from pop.loader import LoadedMod

_HUB_SUB_CACHE = {}


def resolve(hub, ref: str):
    def gen_sub():
        call_path = ref.split(".")
        method_name = call_path[-1]
        hub_api_sub = hub
        # TODO: The first segment of the call path is ignored (assuming it's hub.** call).
        for c in call_path[1:]:
            hub_api_sub = getattr(hub_api_sub, c)

        _HUB_SUB_CACHE[ref] = HubContractMod(hub, hub_api_sub, method_name, ref)
        return _HUB_SUB_CACHE[ref]

    return _HUB_SUB_CACHE.get(ref) or gen_sub()


class HubContractMod(LoadedMod):
    def __init__(self, hub, hub_method, method_name, ref):
        super().__init__(name=ref)
        self._hub = hub
        self._hub_method = hub_method
        self._method_name = method_name

    @property
    def signature(self):
        return signature(self.__call__)

    def _missing(self, item: str):
        return self

    async def __call__(self, ctx, *args, **kwargs):
        result = {"result": True, "ret": None, "comment": []}

        try:
            response = await self._hub_method(ctx, *args, **kwargs)
            if not response:
                result["result"] = False
                return result

            result["result"] = response["result"]
            result["ret"] = response["ret"]
            result["comment"] += response["comment"]

        except Exception as e:
            result["result"] = False
            result["comment"].append(str(e))

        return result
