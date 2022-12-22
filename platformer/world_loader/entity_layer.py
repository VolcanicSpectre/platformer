"""Provides an interface for loading entities from and LDTK entity layer
"""
from dataclasses import dataclass
from platformer.world_loader.entity import Entity
from platformer.world_loader.layer import Layer, set_attr


@dataclass(frozen=True)
class EntityLayer(Layer):
    """An interface for loading entities from an LDTK entity layer"""

    def __post_init__(self):
        super().__post_init__()
        entities: list[Entity] = [
            Entity(entity_instance) for entity_instance in self.data["entityInstances"]
        ]

        set_attr(self, "entities", entities)
