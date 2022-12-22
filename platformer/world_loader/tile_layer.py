from pygame import Rect
from platformer.world_loader.tileset import Tileset
from platformer.world_loader.layer import Layer, set_attr
from platformer.world_loader.map_tile import MapTile


class TileLayer(Layer):
    tileset: Tileset

    def __post_init__(self):
        super().__post_init__()
        grid_tiles: list[MapTile] = []
        for tile_instance in self.data["gridTiles"]:
            grid_tiles.append(
                MapTile(
                    self.tileset.get_tile_from_id(tile_instance["t"]),
                    Rect(
                        tile_instance["px"][0],
                        tile_instance["px"][1],
                        self.tileset.tile_grid_size,
                        self.tileset.tile_grid_size,
                    ),
                )
            )

        set_attr(self, "grid_tiles", grid_tiles)
