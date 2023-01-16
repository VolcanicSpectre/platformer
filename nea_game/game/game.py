from __future__ import annotations
from os import listdir
from pathlib import Path
import typing
import pygame
from pygame.event import Event
from pygame import Rect, Surface
from nea_game.game.camera import Camera
from nea_game.gui.window import Window
from nea_game.menu.background_layer import BackgroundLayer
from nea_game.ldtk_world_loader.world import World
from nea_game.player.player import Player

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
        background_image_layers_path: Path,
    ):
        super().__init__(screen, display_surface)
        self.parent = parent
        self.config = self.parent.config

        self.world_number = world_number
        self.level_number = level_number

        self.world = World(
            self.world_number,
            self.config.directories["worlds"],
            self.screen.get_width() // self.display_surface.get_width(),
        )

        self.background_layers = [
            BackgroundLayer(pygame.image.load(background_image_layers_path / filename))
            for filename in sorted(listdir(background_image_layers_path))
            if filename.endswith(".png") and filename not in ["-1.png", "2.png"]
        ]

        self.player = Player(
            self.config.directories["player"],
            self.world.levels[0].level_data,
            self.config.key_bindings,
            self.config.internal_fps,
            17,
            160,
        )
        self.camera = Camera(
            self.world.levels[0].height,
            self.world.levels[0].width,
            self.display_surface.get_height(),
            self.display_surface.get_width(),
        )

    def event_handler(self, events: list[Event]):
        self.player.event_handler(events)

    def update(self, dt: float):
        self.player.update(dt)
        self.camera.update(self.player.rect)

    def draw(self):
        self.display_surface.fill((0, 0, 0))

        self.display_surface.blit(self.background_layers[0].image, (0, 0))
        for background_layer in self.background_layers[1:2]:
            self.display_surface.blit(background_layer.get_new_sub_image(), (0, 0))

        pygame.transform.scale(
            self.display_surface, self.screen.get_size(), dest_surface=self.screen
        )

        for tile in self.world.levels[0].level_data:
            self.screen.blit(
                tile.image,
                (
                    tile.rect.left - self.camera.scroll_x,
                    tile.rect.top - self.camera.scroll_y,
                ),
            )

        self.player.renderer.render_entity(
            "idle",
            self.screen,
            self.player.rect.x - self.camera.scroll_x,
            self.player.rect.y - self.camera.scroll_y,
        )

        pygame.display.flip()
