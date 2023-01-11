from __future__ import annotations
import typing
import pygame
from pygame import Rect, Surface
from nea_game.game.camera import Camera
from nea_game.gui.window import Window
from nea_game.ldtk_world_loader.world import World

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

        self.world = World(self.world_number, self.config.directories["worlds"])
        self.camera = Camera(
            self.world.levels[0].height,
            self.world.levels[0].width,
            self.display_surface.get_height(),
            self.display_surface.get_width(),
        )

    def update(self, dt: float):
        self.camera.update(Rect((39, 200), (4, 8)))

    def draw(self):
        self.display_surface.fill((0, 0, 0))
        for tile in self.world.levels[0].level_data:
            self.display_surface.blit(
                tile.image,
                (
                    tile.rect.left - self.camera.get_scroll_x(),
                    tile.rect.top - self.camera.get_scroll_y(),
                ),
            )

        pygame.transform.scale(
            self.display_surface, self.screen.get_size(), dest_surface=self.screen
        )
        pygame.display.flip()
