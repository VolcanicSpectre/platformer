from pygame.event import Event
import pygame
from nea_game.components.base_component import BaseComponent
from nea_game.player.player_action_space import PlayerActionSpace
from nea_game.calc.vector2d import Vector2D


class Input(BaseComponent):
    """Provides an interface for accessing the inputs of a player given actions"""

    actions: dict[PlayerActionSpace, int]

    def __init__(
        self, action_space: type[PlayerActionSpace], action_bindings: list[int]
    ):
        """Summary

        Args:
            action_space (type[PlayerActionSpace]): An Enum for each possible action the player can make
            action_bindings (list[int]): The binding for each corresponding action in action_space
        """
        self.action_space = action_space

        self.actions = dict(zip(list(self.action_space), action_bindings))

        self.actions_performed_on_current_frame = {
            action: False for action in list(self.action_space)
        }

    def get_axis_raw(self) -> Vector2D:
        """Calculates the vector of the directional inputs based on the bindings of the actions UP, DOWN, LEFT, RIGHT. The value for both axis will be either -1, 0 or 1.

        Returns:
            Vector2D: The vector of the directional inputs"""

        horizontal = (
            -1
            if pygame.key.get_pressed()[self.actions[self.action_space.LEFT]]
            else 1
            * (
                pygame.key.get_pressed()[self.actions[self.action_space.LEFT]]
                ^ pygame.key.get_pressed()[self.actions[self.action_space.RIGHT]]
            )
        )

        vertical = (
            1
            if pygame.key.get_pressed()[self.actions[self.action_space.DOWN]]
            else -1
            * (
                pygame.key.get_pressed()[self.actions[self.action_space.DOWN]]
                ^ pygame.key.get_pressed()[self.actions[self.action_space.UP]]
            )
        )

        return Vector2D(horizontal, vertical)

    def update_actions_performed_on_current_frame(self, events: list[Event]):
        """Updates the dictionary corresponding to the actions performed on the current frame"""

        self.actions_performed_on_current_frame = {
            action: False for action in self.action_space
        }
        for event in events:
            if event.type == pygame.KEYDOWN:
                for action, binding in self.actions.items():
                    if event.key == binding:
                        self.actions_performed_on_current_frame[action] = True

    def get_action_down(self, action: PlayerActionSpace) -> bool:
        """Returns true during the frame the user starts pressing down the key identified by the action action enum parameter.

        Args:
            action (Enum): The action that is being checked

        Returns:
            bool: Whether that action was performed that frame
        """
        return self.actions_performed_on_current_frame[action]
