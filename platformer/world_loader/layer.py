"""A base class for an LDTK layer"""
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Layer:
    """Base class for an LDTK layer"""

    data: dict[str, Any]

    def __post_init__(self):
        set_attr(self, "grid_height", self.data["__cHei"])
        set_attr(self, "grid_width", self.data["__cWid"])
        set_attr(self, "grid_size", self.data["__gridSize"])
        set_attr(self, "identifer", self.data["__identifer"])
        set_attr(self, "_type", self.data["__type"])


def set_attr(self: Layer, name: str, val: Any):
    """Frozen dataclasses have an overwrittend __setattr__,"""
    object.__setattr__(self, name, val)
