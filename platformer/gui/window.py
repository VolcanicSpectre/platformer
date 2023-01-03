import pygame
from pygame.mouse import get_pos as get_mouse_pos, get_pressed as get_mouse_pressed
from pygame import Surface
from platformer.gui.button import Button


class Window:
    screen: Surface
    display_surface: Surface
    buttons: list[Button]

    def __init__(self, screen: Surface, display_surface: Surface):

        self.screen = screen
        self.display_surface = display_surface
        self.buttons = []

    def update(self):
        """Updates each button element of the window"""
        mouse_pos: tuple[int, int] = get_mouse_pos()
        mouse_clicked = get_mouse_pressed()[0]
        for button in self.buttons:
            button.update(mouse_pos, mouse_clicked)

    def draw(self):
        """Draws each button element of the window"""
        self.display_surface.fill((0, 0, 0))
        for button in self.buttons:
            self.display_surface.blit(button.current_image, button.rect.topleft)

        pygame.transform.scale(
            self.display_surface, self.screen.get_size(), dest_surface=self.screen
        )
        pygame.display.flip()
