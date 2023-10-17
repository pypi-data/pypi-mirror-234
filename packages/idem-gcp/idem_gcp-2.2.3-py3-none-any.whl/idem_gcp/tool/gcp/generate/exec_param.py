from enum import Enum


class ExecParam(Enum):
    GET_ITEMS = ("get_items", True)
    SCOPED_FUNCTIONS = ("scoped_functions", None)
    PROCESS_RESOURCE_ID_PARAM = ("process_resource_id_param", True)
    PATH_PARAM_ALIASES = ("path_param_aliases", None)
    SANITIZE_PARAM = ("sanitize_param", True)

    def __init__(self, key, default_value):
        self.key = key
        self.default_value = default_value

    def __eq__(self, obj):
        return self.name == obj.name

    def __hash__(self):
        return hash(self.name)
