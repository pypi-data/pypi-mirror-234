from dataclasses import dataclass


@dataclass
class Finding:
    schema_path: str
    description: str
    is_breaking: bool

    def __str__(self):
        breaking_text = "breaking" if self.is_breaking else "non-breaking"
        return f"{self._schema_path} - {self.description} (a {breaking_text} change)"

    @classmethod
    def breaking(cls, schema_path, description):
        return Finding(
            schema_path=schema_path, description=description, is_breaking=True
        )

    @classmethod
    def non_breaking(cls, schema_path, description):
        return Finding(
            schema_path=schema_path, description=description, is_breaking=False
        )


# class EnhancedJSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if dataclasses.is_dataclass(o):
#             return dataclasses.asdict(o)
#         return super().default(o)
