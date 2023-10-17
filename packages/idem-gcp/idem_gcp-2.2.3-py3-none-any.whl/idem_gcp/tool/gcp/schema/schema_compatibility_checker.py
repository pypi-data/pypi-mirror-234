from typing import Dict
from typing import Set

import deepdiff

from idem_gcp.tool.gcp.schema.results_collector import ResultsCollector


def check(
    hub, current_schema: Dict, base_schema: Dict, essential_resources: Set[str] = None
) -> ResultsCollector:
    collector = ResultsCollector()
    exclude_paths = set()

    current_resources = _enumerate_resources(current_schema)
    base_resources = _enumerate_resources(base_schema)

    if current_resources != base_resources:
        removed = base_resources.difference(current_resources)
        if removed:
            for resource in removed:
                collector.add_breaking(
                    schema_path=f"root['{resource}']", description="Resource removed"
                )
                exclude_paths.add(rf"root\[.*{resource}.*\]")

        added = current_resources.difference(base_resources)
        if added:
            for resource in added:
                collector.add_non_breaking(
                    schema_path=f"root['{resource}']", description="Resource added"
                )
                exclude_paths.add(rf"root\[.*{resource}.*\]")

    for k in current_schema.keys():
        exclude = {
            key
            for key in current_schema[k].keys()
            if key not in ["parameters", "return_annotation"]
        }
        for key in exclude:
            exclude_paths.add(rf"root\[.*\]\['{key}'\]")

    changes = deepdiff.DeepDiff(
        base_schema, current_schema, exclude_regex_paths=list(exclude_paths)
    )

    for v in changes.get("dictionary_item_added") or []:
        collector.add_non_breaking(
            schema_path=v, description=f"{_description_for(v, 'added')}"
        )

    for v in changes.get("dictionary_item_removed") or []:
        collector.add_breaking(
            schema_path=v, description=f"{_description_for(v, 'removed')}"
        )

    for v in changes.get("values_changed") or []:
        collector.add_breaking(
            schema_path=v, description=f"{_description_for(v, 'changed')}"
        )

    return collector


def _enumerate_resources(schema: Dict) -> Set[str]:
    return {".".join(s.split(".")[2:-1]) for s in schema.keys()}


def _description_for(change: str, op: str) -> str:
    parts = [x.rstrip("]") for x in change.split("[")]
    if parts[0] == "root":
        depth = len(parts)
        if depth == 2:
            return f"{op} method {parts[1]}"
        elif depth == 3:
            return f"{op} {parts[1]} method's {parts[2]} property"
        elif depth == 4:
            return f"{op} parameter {parts[3]}"
        elif depth == 5:
            return f"{op} {parts[3]} parameter's {parts[4]} property"

    return f"Cannot parse change: {change}"
