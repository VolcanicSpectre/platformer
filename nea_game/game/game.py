from __future__ import annotations
import typing
import pygame
from pygame import Surface
from nea_game.gui.window import Window

if typing.TYPE_CHECKING:
    from nea_game.nea_game import NeaGame


class Game(Window):
    def __init__(
        self,
        parent: NeaGame,
        screen: Surface,
        display_surface: Surface,
        world_number: int,
        level_number: int,
    ):
        super().__init__(screen, display_surface)
        self.parent = parent
        self.config = self.parent.config

        self.world_number = world_number
        self.level_number = level_number

        self.world = LdtkWorld(self.config, self.world_number)

        self.current_ldtk_level = self.world.levels[self.level_number - 1]

    def update(self, dt: float):
        pass

    def draw(self):
        self.display_surface.fill((0, 0, 0))
        for tile_layer in self.current_ldtk_level.tile_layers:
            for tile in tile_layer.grid_tiles:
                self.display_surface.blit(tile.image, tile.rect.topleft)

        pygame.transform.scale(
            self.display_surface, self.screen.get_size(), dest_surface=self.screen
        )
        pygame.display.flip()
