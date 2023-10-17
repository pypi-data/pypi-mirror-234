from enum import Enum


class Scope(Enum):
    GLOBAL = "globalFunction"
    REGIONAL = "regionalFunction"
    ZONAL = "zonalFunction"

    def __init__(self, key):
        self.key = key

    def __eq__(self, obj):
        return self.name == obj.name

    def __hash__(self):
        return hash(self.name)
