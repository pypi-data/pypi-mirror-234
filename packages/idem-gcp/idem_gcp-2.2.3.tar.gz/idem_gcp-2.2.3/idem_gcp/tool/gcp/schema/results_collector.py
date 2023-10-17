import json

import yaml
from yaml import SafeDumper


class ResultsCollector:
    @property
    def findings(self):
        return self._findings

    @property
    def base_revision(self):
        return self._base_revision

    @property
    def current_revision(self):
        return self._current_revision

    def __init__(self, current_revision=None, base_revision=None):
        self._findings = []
        self._current_revision = current_revision
        self._base_revision = base_revision

    def has_breaking_finding(self):
        return (
            len([finding for finding in self.findings if finding.get("is_breaking")])
            > 0
        )

    def revisions(self, current_revision, base_revision):
        self._current_revision = current_revision
        self._base_revision = base_revision
        return self

    def add_breaking(self, schema_path, description):
        self._findings.append(
            {
                "schema_path": schema_path,
                "description": description,
                "is_breaking": True,
            }
        )

    def add_non_breaking(self, schema_path, description):
        self._findings.append(
            {
                "schema_path": schema_path,
                "description": description,
                "is_breaking": False,
            }
        )

    def report_as_json(self):
        report = {
            "base_revision": self.base_revision,
            "current_revision": self.current_revision,
            "findings": self.findings,
        }
        return json.dumps(report, indent=4)

    def report_as_yaml(self):
        report = {
            "base_revision": self.base_revision,
            "current_revision": self.current_revision,
            "findings": self.findings,
        }
        return yaml.dump(report, Dumper=SafeDumper)
