from typing import Any
from entity_layer import EntityLayer
from tile_layer import TileLayer


class Level:
    def __init__(self, data: dict[str, Any]):
        self.data = data
        self.identifer: str = self.data["identifer"]

        self.px_height: int = self.data["pxHei"]
        self.px_width: int = self.data["pxWid"]

        self.world_x: int = self.data["worldX"]
        self.world_y: int = self.data["worldY"]

        self.entity_layer = None
        self.tile_layer = None

        for layer_instance in self.data["layerInstances"]:
            if (
                layer_instance["__identifier"] == "Entities"
                and self.entity_layer is not None
            ):
                self.entity_layer = EntityLayer(layer_instance)

            if (
                layer_instance["__identifier"] == "Tiles"
                and self.tile_layer is not None
            ):
                self.tile_layer = TileLayer(layer_instance)
