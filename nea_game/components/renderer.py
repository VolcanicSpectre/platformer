import pygame
from nea_game.states.player_state import PlayerState


class StaticRenderer:
    def __init__(self, static_frame: pygame.Surface):
        """Creates a StaticRenderer component for a static object

        Args:
            static_frame (pygame.Surface): The static frame to be rendered
        """
        self.static_frame = static_frame

    def render_entity(self, surface: pygame.Surface, x: float, y: float):
        """Renders the static frame onto the surface at the given position

        Args:
            surface (pygame.Surface): The surface that the frame is rendered onto
            x (int): The x position that the static frame is rendered onto
            y (int): The y position that the static frame is rendered onto
        """
        surface.blit(self.static_frame, (x, y))


class AnimatedRenderer:
    def __init__(self, frames: dict[str, list[pygame.Surface]]):
        """Creates an AnimatedRenderer component for an animated object

        Args:
            frames (list[pygame.Surface]): The list of each possible frame for the animated object
            current_frame_index (int, optional): If specified the starting frame will be the frame specified at the given index, otherwise the first one is selected
        """
        self.frames = frames

    def render_entity(
        self,
        state: PlayerState,
        flip_x: bool,
        surface: pygame.Surface,
        x: float,
        y: float,
    ):
        """Renders the current frame onto the surface at the given position
        Args:
            state_name (str): The current state of the entity
            surface (pygame.Surface): The surface that the frame is rendered onto
            x (int): The x position that the frame is rendered onto
            y (int): The y position that the frame is rendered onto
        """
        surface.blit(
            pygame.transform.flip(
                self.frames[state.state_name][state.animation_index], flip_x, False
            ),
            (x, y),
        )
