from __future__ import annotations
from json import dump, load as load_json
from os import listdir
from pathlib import Path
import typing
import pygame
from pygame.image import load
from pygame.mouse import get_pos as get_mouse_pos, get_pressed as get_mouse_pressed
from pygame import Surface
from nea_game.menu.action_button import ActionButton
from nea_game.gui.button import Button
from nea_game.gui.window import Window

if typing.TYPE_CHECKING:
    from nea_game.nea_game import NeaGame


class Settings(Window):
    buttons: dict[str, Button]
    action_buttons: dict[str, ActionButton]

    def __init__(
        self,
        parent: NeaGame,
        screen: Surface,
        display_surface: Surface,
        action_button_folder_path: Path,
        key_bindings: list[int],
    ):
        super().__init__(screen, display_surface)
        self.parent = parent

        self.title_image = load(
            action_button_folder_path.parent / "settings_title.png"
        ).convert_alpha()

        self.text = load(
            action_button_folder_path.parent / "settings_text.png"
        ).convert_alpha()

        self.buttons = {}
        self.action_buttons = {}
        for button in listdir(action_button_folder_path.parent / "buttons/settings"):
            self.buttons[button] = Button(
                (action_button_folder_path.parent / "buttons/settings") / button
            )

        for action_button, key_binding in zip(
            listdir(action_button_folder_path), key_bindings
        ):
            self.action_buttons[action_button] = ActionButton(
                action_button_folder_path / action_button,
                action_button_folder_path.parent / "keys",
                key_binding,
            )

        self.buttons["back"].rect.bottomright = (383, 215)
        self.action_buttons["up"].rect.topleft = (20, 20)
        self.action_buttons["down"].rect.topleft = (20, 60)
        self.action_buttons["left"].rect.topleft = (20, 100)
        self.action_buttons["right"].rect.topleft = (20, 140)
        self.action_buttons["dash"].rect.topleft = (20, 180)

    def update(self, dt: float):
        mouse_pos: tuple[int, int] = get_mouse_pos()
        scaled_mouse_pos: tuple[int, int] = (
            mouse_pos[0] // self.scale_factor,
            mouse_pos[1] // self.scale_factor,
        )
        mouse_clicked = get_mouse_pressed()[0]

        for button in self.buttons.values():
            button.update(scaled_mouse_pos, mouse_clicked, dt)

        for action_button in self.action_buttons.values():
            if action_button.click_timer >= 0:

                other_binds = [
                    other_action_button.key
                    for other_action_button in self.action_buttons.values()
                    if other_action_button != action_button
                ]

                for event in pygame.event.get():
                    action_button.update(
                        scaled_mouse_pos, mouse_clicked, 0, other_binds, event
                    )

            action_button.update(scaled_mouse_pos, mouse_clicked, dt)

        if self.buttons["back"].clicked:
            self.save_controls()
            self.parent.show_window("main_menu")

    def draw(self):
        self.display_surface.fill((8, 169, 252))
        self.display_surface.blit(self.title_image, (195, 5))
        self.display_surface.blit(self.text, (150, 44))

        for button in self.buttons.values():
            self.display_surface.blit(button.current_image, button.rect.topleft)

        for action_button in self.action_buttons.values():
            self.display_surface.blit(
                action_button.current_image, action_button.rect.topleft
            )

            self.display_surface.blit(
                action_button.key_image,
                (action_button.rect.right + 10, action_button.rect.top - 12),
            )

        pygame.transform.scale(
            self.display_surface, self.screen.get_size(), dest_surface=self.screen
        )
        pygame.display.flip()

    def save_controls(self):
        with (self.parent.config.directories["platformer"] / "config.json").open(
            mode="r"
        ) as settings_json:
            new_settings_json = load_json(settings_json)

            new_settings_json["key_bindings"] = [
                action_button.key for action_button in self.action_buttons.values()
            ]

        with (self.parent.config.directories["platformer"] / "config.json").open(
            mode="w"
        ) as settings_json:
            dump(new_settings_json, settings_json, indent=4)

        self.parent.config.reload()
