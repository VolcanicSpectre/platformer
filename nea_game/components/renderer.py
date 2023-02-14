from pygame import Surface
import pygame
from nea_game.states.player_state import PlayerState


class StaticRenderer:
    """Provides functionality for rendering a static entity"""

    static_frame: Surface

    def __init__(self, static_frame: Surface):
        """Creates a StaticRenderer component for a static object

        Args:
            static_frame (Surface): The static frame to be rendered
        """
        self.static_frame = static_frame

    def render_entity(self, surface: Surface, x: float, y: float):
        """Renders the static frame onto the surface at the given position

        Args:
            surface (Surface): The surface that the frame is rendered onto
            x (int): The x position that the static frame is rendered at
            y (int): The y position that the static frame is rendered at
        """
        surface.blit(self.static_frame, (x, y))


class AnimatedRenderer:
    """Provides functionality for rendering an animated entity with multiple states"""

    frames: dict[str, list[Surface]]

    def __init__(self, frames: dict[str, list[Surface]]):
        """Creates an AnimatedRenderer component for an animated object

        Args:
            frames (dict[str, list[Surface]]): The list of each possible frame for the animated object
        """
        self.frames = frames

    def render_entity(
        self,
        state: PlayerState,
        flip_x: bool,
        surface: Surface,
        x: float,
        y: float,
    ):
        """Renders the current frame onto the surface at the given position
        Args:
            state_name (str): The current state of the entity
            surface (Surface): The surface that the frame is rendered onto
            x (int): The x position that the frame is rendered onto
            y (int): The y position that the frame is rendered onto
        """
        surface.blit(
            pygame.transform.flip(
                self.frames[state.state_name][state.animation_index], flip_x, False
            ),
            (x, y),
        )
