from pygame.event import Event
from pygame import Surface


class Window:
    screen: Surface
    display_surface: Surface

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

    def event_handler(self, event: Event):
        """Passes down the event to the event_handler for any relvant operations

        Args:
            event (Event): A pygame event
        """

    def update(self, dt: float):
        """Updates window"""

    def draw(self):
        """Draws window"""
