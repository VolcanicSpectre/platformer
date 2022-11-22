import pygame

from base_component import BaseComponent
from player.player_action_space import PlayerActionSpace
from calc.vector2d import Vector2D

class Input(BaseComponent):
	def __init__(self, action_space: type[PlayerActionSpace], action_bindings: list[int]):
		"""Summary
		
		Args:
		    action_space (type[PlayerActionSpace]): An Enum for each possible action the player can make
		    action_bindings (list[int]): The binding for each corresponding action in action_space
		"""
		self.__action_space = action_space

		self.__actions = {action: binding for action, binding in zip([member.value for member in self.__action_space], action_bindings)}
		self.__actions_performed_on_current_frame = {action: False for action in [member.value for member in self.__action_space]}
	
	def get_axis_raw(self) -> Vector2D:
		"""Calculates the vector of the directional inputs based on the bindings of the actions UP, DOWN, LEFT, RIGHT. The value for both axis will be either -1, 0 or 1.
		
		Returns:
		    Vector2D: The vector of the directional inputs		"""
		horizontal = -1 if pygame.key.get_pressed()[self.__actions[self.__action_space.LEFT]] else 1 * (pygame.key.get_pressed()[self.__actions[self.__action_space.LEFT]] ^ pygame.key.get_pressed()[self.__actions[self.__action_space.RIGHT]])

		vertical = -1 if pygame.key.get_pressed()[self.__actions[self.__action_space.DOWN]] else 1 * (pygame.key.get_pressed()[self.__actions[self.__action_space.DOWN]] ^ pygame.key.get_pressed()[self.__actions[self.__action_space.UP]])

		return Vector2D(horizontal, vertical)

	def update_actions_performed_on_current_frame(self, event: pygame.Event) -> None:
		"""Updates the dictionary corresponding to the actions performed on the current frame
		
		Args:
		    event (pygame.Event): An event
		"""
		self.__actions_performed_on_current_frame = {action: False for action in self.__action_space}
		if event.type == pygame.KEYDOWN:
			for action, binding in self.__actions.items():
				if event.key == binding:
					self.__actions_performed_on_current_frame[action] = True

	def get_key_down(self, action: PlayerActionSpace) -> bool:
		"""Returns true during the frame the user starts pressing down the key identified by the action action enum parameter.
		
		Args:
		    action (Enum): The action that is being checked 
		
		Returns:
		    bool: Whether that action was performed that frame
		"""
		return self.__actions_performed_on_current_frame[action]


