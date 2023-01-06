from dataclasses import dataclass
from pygame import Rect
from nea_game.world_loader.tileset import Tileset
from nea_game.world_loader.layer import Layer, set_attr
from nea_game.world_loader.map_tile import MapTile


@dataclass(frozen=True)
class TileLayer(Layer):
    tileset: Tileset

    def __post_init__(self):
        super().__post_init__()
        grid_tiles: list[MapTile] = []
        for tile_instance in self.data["gridTiles"]:
            grid_tiles.append(
                MapTile.from_tileset_tile(
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
