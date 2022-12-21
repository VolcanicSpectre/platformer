"""Provides a class to store the relevant data about an LDTK entity instance
"""
from dataclasses import dataclass
from typing import Any


@dataclass
class Entity:
    """A class to store the relevant data about an LDTK entity instance"""

    data: dict[str, Any]

    def __post_init__(self) -> None:
        set_attr(self, "position", (self.data["position"][0], self.data["position"][1]))
        set_attr(self, "identifier", self.data["__identifier"])
        set_attr(self, "height", self.data["height"])
        set_attr(self, "width", self.data["width"])

        custom_data: dict[str, Any] = {}
        for field_instance in self.data["fieldInstances"]:
            custom_data[field_instance["__identifier"]] = field_instance["__value"]
            set_attr(self, "custom_data", custom_data)


def set_attr(self: Entity, name: str, val: Any):
    """Frozen dataclasses have an overwrittend __setattr__,"""
    object.__setattr__(self, name, val)
