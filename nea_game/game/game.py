from __future__ import annotations
import itertools
from json import dump, load as load_json
from os import listdir
from pathlib import Path
import typing
import pygame
from pygame.event import Event
from pygame import Surface
from nea_game.game.camera import Camera
from nea_game.game.render_object import RenderObject
from nea_game.gui.window import Window
from nea_game.menu.background_layer import BackgroundLayer
from nea_game.menu.pause_menu import Pause
from nea_game.ldtk_world_loader.level_tile import LevelTile
from nea_game.ldtk_world_loader.world import World
from nea_game.player.player_action_space import PlayerActionSpace
from nea_game.player.player import Player
from nea_game.config import NeaGameConfig
from nea_game.circular_queue import CircularQueue

if typing.TYPE_CHECKING:
    from nea_game.nea_game import NeaGame


class Game(Window):
    """Creates a window that allows a player to play the specified level, when the level is beaten the next one is unlocked by writing to the config.json file"""

    parent: NeaGame
    config: NeaGameConfig
    world_identifier: str
    level_identifier: str
    world: World
    render_queue: CircularQueue[RenderObject]
    background_layers: list[BackgroundLayer]
    player: Player
    camera: Camera

    def __init__(
        self,
        parent: NeaGame,
        screen: Surface,
        display_surface: Surface,
        world_identifier: str,
        level_identifier: str,
        background_image_layers_path: Path,
    ):
        super().__init__(screen, display_surface)
        self.parent = parent
        self.config = self.parent.config

        self.world_identifier = world_identifier
        self.level_identifier = level_identifier

        self.world = World(
            self.world_identifier,
            self.config.directories["worlds"],
            self.config.chunk_size,
        )
        self.render_queue = CircularQueue(
            400, RenderObject
        )  # A: Circular queue to model render queue

        self.background_layers = [
            BackgroundLayer(pygame.image.load(background_image_layers_path / filename))
            for filename in sorted(listdir(background_image_layers_path))
            if filename.endswith(".png") and filename not in ["-1.png", "2.png"]
        ]

        self.player = Player(
            self.config.directories["player"],
            self.world.levels[self.level_identifier].level_data["chunks"],
            self.config.key_bindings,
            self.config.internal_fps,
            self.world.levels[self.level_identifier].level_data["player_position"],
        )
        self.camera = Camera(
            self.world.levels[self.level_identifier].height,
            self.world.levels[self.level_identifier].width,
            self.display_surface.get_height(),
            self.display_surface.get_width(),
        )

    def event_handler(self, events: list[Event]):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                window = Pause(
                    self.parent,
                    self.screen,
                    self.display_surface,
                    self.parent.config.directories["gui"] / "pause",
                )
                self.parent.windows["pause"] = window
                self.parent.show_window("pause")
        self.player.event_handler(events)

    def update(self, delta_time: float):
        if self.has_level_finished():
            if self.parent.is_transition_done:
                self.end_level()
                self.parent.show_window("level_selection")

            elif not self.parent.is_transitioning:
                self.parent.set_transitioning(
                    self.parent.transition_circle_out,
                    2,
                    tuple(
                        map(
                            lambda x: x * self.scale_factor,
                            (
                                self.player.rect.centerx - self.camera.scroll_x,
                                self.player.rect.centery - self.camera.scroll_y,
                            ),
                        )
                    ),
                )

            return

        if not self.player.is_alive(self.camera.height):
            if self.player.input_.get_action_down(PlayerActionSpace.DASH):
                self.parent.is_transition_done = True
                window = Game(
                    self.parent,
                    self.screen,
                    self.display_surface,
                    self.world_identifier,
                    self.level_identifier,
                    self.parent.config.directories["background"] / "sky_mountain",
                )
                self.parent.windows["game"] = window
                self.parent.show_window("game")

            if self.parent.is_transition_done:
                self.parent.show_window("level_selection")
                self.parent.sound_manager.play_sound("click")

            elif not self.parent.is_transitioning:
                self.parent.set_transitioning(
                    self.parent.transition_circle_out,
                    1,
                    tuple(
                        map(
                            lambda x: x * self.scale_factor,
                            (
                                self.player.rect.centerx - self.camera.scroll_x,
                                self.player.rect.centery - self.camera.scroll_y,
                            ),
                        )
                    ),
                )

        if not self.parent.is_transitioning:
            self.parent.is_transition_done = False
            self.player.update(delta_time)

        if self.player.state_machine.current_state == self.player.jump_state:
            self.parent.sound_manager.play_sound("jump")
        self.camera.update(self.player.rect)

    def has_level_finished(self) -> bool:
        """Checks if the level has finished

        Returns:
            bool: Whether the level has finished or not
        """
        if self.player.rect.colliderect(
            self.world.levels[self.level_identifier].level_data["level_finish"].rect
        ):
            return True

        return False

    def end_level(self):
        """Ends the level by unlocking the next level and reloading the config.json file
        """
        level_finish = self.world.levels[self.level_identifier].level_data[
            "level_finish"
        ]
        with (self.parent.config.directories["platformer"] / "config.json").open(
            mode="r"
        ) as settings_json:
            new_settings_json = load_json(settings_json)
            if level_finish.new_world:
                new_world = str(int(self.world_identifier) + 1)
            else:
                new_world = self.world_identifier
            new_level = level_finish.next_level_identifier[1:].replace("_", "-")
            new_settings_json["unlocked_levels"][new_world + new_level] = True

        with (self.parent.config.directories["platformer"] / "config.json").open(
            mode="w"
        ) as settings_json:
            dump(new_settings_json, settings_json, indent=4)

        self.parent.config.reload()

    def get_visible_chunks(self) -> list[list[LevelTile]]:
        """Returns the list of LevelTiles that are currently on the screen

        Returns:
            list[list[LevelTile]]: The LevelTile list for each chunk that is visible on the screen
        """
        ###B: Two Dimensional List###
        visible_chunks: list[list[LevelTile]] = []

        for chunk_x, chunk_y in self.world.levels[self.level_identifier].level_data[
            "chunks"
        ]:
            if pygame.Rect(
                chunk_x * self.config.chunk_size,
                chunk_y * self.config.chunk_size,
                self.config.chunk_size,
                self.config.chunk_size,
            ).colliderect(
                pygame.Rect(
                    self.camera.scroll_x,
                    self.camera.scroll_y,
                    self.config.internal_resoloution[0],
                    self.config.internal_resoloution[1],
                )
            ):
                visible_chunks.append(
                    self.world.levels[self.level_identifier].level_data["chunks"][
                        (chunk_x, chunk_y)
                    ]
                )

        return visible_chunks

    def update_render_queue(self):
        """Updates the render queue to only render the tiles in chunks that are currently visible
        """
        for chunk in self.get_visible_chunks():
            for tile in chunk:
                self.render_queue.enqueue(
                    RenderObject(tile.rect.x, tile.rect.y, tile.image)
                )

    def draw(self):
        self.display_surface.fill((0, 0, 0))
        self.update_render_queue()

        self.display_surface.blit(self.background_layers[0].image, (0, 0))
        for background_layer in self.background_layers[1:2]:
            self.display_surface.blit(background_layer.get_new_sub_image(), (0, 0))

        while not self.render_queue.is_empty():
            render_object = self.render_queue.dequeue()
            self.display_surface.blit(
                render_object.image,
                (
                    render_object.x - self.camera.scroll_x,
                    render_object.y - self.camera.scroll_y,
                ),
            )

        self.player.renderer.render_entity(
            self.player.state_machine.current_state,
            self.player.direction == -1,
            self.display_surface,
            self.player.rect.x - self.camera.scroll_x,
            self.player.rect.y - self.camera.scroll_y,
        )

        pygame.transform.scale(
            self.display_surface, self.screen.get_size(), dest_surface=self.screen
        )
        if self.parent.is_transitioning:
            self.parent.run_transition()
        pygame.display.flip()
