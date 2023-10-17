import dataclasses
from dataclasses import dataclass
from typing import Any
from typing import Dict

from idem_gcp.tool.gcp.generate.exec_param import ExecParam


@dataclass
class ExecutionContext:
    resource_type: str  # e.g. compute.instance
    method_name: str
    method_params: Dict[str, Any]
    exec_params: Dict[ExecParam, Any] = dataclasses.field(default_factory=dict)
    method: Any = None  # the resolved method to be executed
    response: Dict[str, Any] = None

    def __post_init__(self):
        self.fill_default_exec_params()

    def fill_default_exec_params(self):
        if self.exec_params is None:
            self.exec_params = dict()
        filled_exec_params = {**self.exec_params}
        for exec_param in ExecParam:
            if exec_param not in self.exec_params:
                filled_exec_params[exec_param] = exec_param.default_value
        self.exec_params = filled_exec_params

    def get_exec_param_value(self, param: ExecParam):
        return self.exec_params.get(param)

    def get_method_param_value(self, param: str):
        return self.method_params.get(param)
