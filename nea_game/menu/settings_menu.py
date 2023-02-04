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
from nea_game.gui.slider import Slider
from nea_game.gui.window import Window

if typing.TYPE_CHECKING:
    from nea_game.nea_game import NeaGame


class Settings(Window):
    buttons: dict[str, Button]
    action_buttons: dict[str, ActionButton]
    sliders: dict[str, Slider]

    def __init__(
        self,
        parent: NeaGame,
        screen: Surface,
        display_surface: Surface,
        path: Path,
        key_bindings: list[int],
    ):
        super().__init__(screen, display_surface)
        self.parent = parent

        self.title_image = load(path / "title.png").convert_alpha()

        self.text = load(path / "text.png").convert_alpha()

        self.music_icon = load(path / "music.png")
        self.sound_icon = load(path / "sound.png")
        self.buttons = {}
        self.action_buttons = {}
        self.sliders = {}

        self.sliders["music_volume"] = Slider(
            path / "sliders/volume",
            0,
            100,
            int(self.parent.config.music_volume * 100),
        )
        self.sliders["sfx_volume"] = Slider(
            path / "sliders/volume",
            0,
            100,
            int(self.parent.config.sfx_volume * 100),
        )
        for button in listdir(path / "buttons"):
            self.buttons[button] = Button((path / "buttons") / button)

        for action_button, key_binding in zip(
            listdir(path / "action_buttons"), key_bindings
        ):
            self.action_buttons[action_button] = ActionButton(
                path / "action_buttons" / action_button,
                path / "keys",
                key_binding,
            )

        self.buttons["back"].rect.bottomright = (383, 215)
        for index, action_button in enumerate(self.action_buttons.values()):
            action_button.rect.topleft = (20, 20 + 40 * index)

        self.sliders["music_volume"].set_topleft(195, 175)
        self.sliders["sfx_volume"].set_topleft(195, 200)

    def update(self, delta_time: float):
        mouse_pos: tuple[int, int] = get_mouse_pos()
        scaled_mouse_pos: tuple[int, int] = (
            mouse_pos[0] // self.scale_factor,
            mouse_pos[1] // self.scale_factor,
        )
        mouse_clicked = get_mouse_pressed()[0]
        for slider in self.sliders.values():
            slider.update(scaled_mouse_pos, mouse_clicked, delta_time)

        for button in self.buttons.values():
            button.update(scaled_mouse_pos, mouse_clicked, delta_time)

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

            action_button.update(scaled_mouse_pos, mouse_clicked, delta_time)

        if self.buttons["back"].clicked:
            self.parent.sound_manager.play_sound("click")
            self.save()
            self.parent.show_window("main_menu")

    def draw(self):
        self.display_surface.fill((8, 169, 252))
        self.display_surface.blit(self.title_image, (195, 5))
        self.display_surface.blit(self.text, (150, 44))
        self.display_surface.blit(self.music_icon, (180, 176))
        self.display_surface.blit(self.sound_icon, (180, 200))
        for slider in self.sliders.values():
            self.display_surface.blit(slider.current_image, slider.rect.topleft)
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

    def save(self):
        with (self.parent.config.directories["platformer"] / "config.json").open(
            mode="r"
        ) as settings_json:
            new_settings_json = load_json(settings_json)

            new_settings_json["music_volume"] = (
                self.sliders["music_volume"].value - 1
            ) / self.sliders["music_volume"].max_value
            new_settings_json["sfx_volume"] = (
                self.sliders["sfx_volume"].value - 1
            ) / self.sliders["sfx_volume"].max_value
            new_settings_json["key_bindings"] = [
                action_button.key for action_button in self.action_buttons.values()
            ]

        with (self.parent.config.directories["platformer"] / "config.json").open(
            mode="w"
        ) as settings_json:
            dump(new_settings_json, settings_json, indent=4)

        self.parent.config.reload()
