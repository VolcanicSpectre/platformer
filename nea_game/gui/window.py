import pygame
from pygame.mouse import get_pos as get_mouse_pos, get_pressed as get_mouse_pressed
from pygame import Surface
from nea_game.gui.button import Button


class Window:
    screen: Surface
    display_surface: Surface
    buttons: dict[str, Button]

    def __init__(self, screen: Surface, display_surface: Surface):

        self.screen = screen
        self.display_surface = display_surface
        self.scale_factor: int = (
            self.screen.get_width() // self.display_surface.get_width()
        )
        if (
            self.scale_factor
            != self.screen.get_height() // self.display_surface.get_height()
        ):
            raise ValueError("Display surface and screen must be proportional")

        self.buttons = {}

    def update(self, dt: float):
        """Updates each button element of the window"""
        mouse_pos: tuple[int, int] = get_mouse_pos()
        scaled_mouse_pos: tuple[int, int] = (
            mouse_pos[0] // self.scale_factor,
            mouse_pos[1] // self.scale_factor,
        )
        mouse_clicked = get_mouse_pressed()[0]
        for button in self.buttons.values():
            button.update(scaled_mouse_pos, mouse_clicked, dt)

    def draw(self):
        """Draws each button element of the window"""
        self.display_surface.fill((0, 0, 0))
        for button in self.buttons.values():
            self.display_surface.blit(button.current_image, button.rect.topleft)

        pygame.transform.scale(
            self.display_surface, self.screen.get_size(), dest_surface=self.screen
        )
        pygame.display.flip()
