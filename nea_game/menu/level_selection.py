from __future__ import annotations
from os import listdir
from pathlib import Path
import typing
import pygame
from pygame.mouse import get_pos as get_mouse_pos, get_pressed as get_mouse_pressed
from pygame import Surface
from nea_game.game.game import Game
from nea_game.gui.button import Button
from nea_game.gui.window import Window

if typing.TYPE_CHECKING:
    from nea_game.nea_game import NeaGame


class LevelSelection(Window):
    buttons: dict[str, Button]
    padding: tuple[int, int]
    spacing: tuple[int, int]

    def __init__(
        self,
        parent: NeaGame,
        screen: Surface,
        display: Surface,
        button_folder_path: Path,
    ):
        super().__init__(screen, display)
        self.parent = parent
        self.button_folder_path = button_folder_path
        self.padding = (30, 50)
        self.spacing = (59, 38)

        self.buttons = {}

        for button in listdir(button_folder_path):
            self.buttons[button] = Button(button_folder_path / button)

        for button_name, button in zip(self.buttons, self.buttons.values()):
            if button_name == "back":
                button.rect.bottomright = (383, 215)
            else:
                world_num = int(button_name[0])
                level_num = int(button_name[2])

                button.rect.topleft = (
                    self.padding[0] + (level_num - 1) * self.spacing[0],
                    self.padding[1] + (world_num - 1) * self.spacing[1],
                )

        for name, unlocked in self.parent.config.unlocked_levels.items():
            if not unlocked:
                self.buttons[name].active_image = self.buttons[name].passive_image
                self.buttons[name].on_click_image = self.buttons[name].passive_image
                self.buttons[name].can_be_clicked = False

    def reload(self):
        self.buttons = {}

        for button in listdir(self.button_folder_path):
            self.buttons[button] = Button(self.button_folder_path / button)

        for button_name, button in zip(self.buttons, self.buttons.values()):
            if button_name == "back":
                button.rect.bottomright = (383, 215)
            else:
                world_num = int(button_name[0])
                level_num = int(button_name[2])

                button.rect.topleft = (
                    self.padding[0] + (level_num - 1) * self.spacing[0],
                    self.padding[1] + (world_num - 1) * self.spacing[1],
                )

        for name, unlocked in self.parent.config.unlocked_levels.items():
            if not unlocked:
                self.buttons[name].active_image = self.buttons[name].passive_image
                self.buttons[name].on_click_image = self.buttons[name].passive_image
                self.buttons[name].can_be_clicked = False

    def update(self, dt: float):
        mouse_pos: tuple[int, int] = get_mouse_pos()
        scaled_mouse_pos: tuple[int, int] = (
            mouse_pos[0] // self.scale_factor,
            mouse_pos[1] // self.scale_factor,
        )
        mouse_clicked = get_mouse_pressed()[0]

        for button in self.buttons.values():
            button.update(scaled_mouse_pos, mouse_clicked, dt)

        if self.buttons["back"].clicked:
            self.parent.sound_manager.play_sound("click")
            self.parent.show_window("main_menu")

        for button_name, button in self.buttons.items():
            if button_name == "back":
                continue
            if button.clicked:
                self.parent.sound_manager.play_sound("click")
                world_and_level = button_name.split("-")
                window = Game(
                    self.parent,
                    self.screen,
                    self.display_surface,
                    world_and_level[0],
                    f"_{world_and_level[1]}",
                    self.parent.config.directories["background"] / "sky_mountain",
                )
                self.parent.windows["game"] = window
                self.parent.show_window("game")
                self.parent.set_transitioning(
                    self.parent.transition_circle_in,
                    1,
                    tuple(
                        map(
                            lambda x: x * self.scale_factor,
                            self.parent.windows["game"].player.rect.center,
                        )
                    ),
                )

    def draw(self):
        self.display_surface.fill((8, 169, 252))

        for button in self.buttons.values():
            self.display_surface.blit(button.current_image, button.rect.topleft)

        pygame.transform.scale(
            self.display_surface, self.screen.get_size(), dest_surface=self.screen
        )
        pygame.display.flip()
