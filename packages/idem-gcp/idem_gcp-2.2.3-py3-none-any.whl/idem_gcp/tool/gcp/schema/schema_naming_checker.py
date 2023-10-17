from typing import Dict

from idem_gcp.tool.gcp.schema.results_collector import ResultsCollector


def check(hub, current_schema: Dict) -> ResultsCollector:
    collector = ResultsCollector()

    for method in current_schema.keys():
        method_name = method.split(".")[-1]
        if method_name in {"field", "make_dataclass"}:
            continue
        method_path = f"root['{method}']"
        if not hub.tool.gcp.case.is_snake_case(method):
            collector.add_breaking(
                schema_path=method_path, description="method name is not in snake_case"
            )
        parameters: Dict = current_schema.get(method).get("parameters") or {}
        for parameter in parameters.keys():
            parameter_path = f"{method_path}['parameters']['{parameter}']"
            if not hub.tool.gcp.case.is_snake_case(parameter):
                collector.add_breaking(
                    schema_path=parameter_path,
                    description="parameter name is not in snake_case",
                )
            if not hub.tool.gcp.case.is_unclashed(parameter):
                collector.add_breaking(
                    schema_path=parameter_path,
                    description="parameter name shadows builtin",
                )

    return collector
