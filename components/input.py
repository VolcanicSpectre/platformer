import pygame
from enum import Enum
from vector2D import Vector2D
from action_space import Actions

class Input:
	def __init__(self, action_space: list[Enum], action_bindings: list[int]):
		self.__action_space = action_space
		self.__actions = {action: binding for action, binding in zip(self.__action_space, action_bindings)}
		self.__actions_performed_on_current_frame = {action: False for action in self.__action_space}
	
	def get_axis_raw(self) -> Vector2D:
		"""Calculates the vector of the directional inputs based on the bindings of the actions UP, DOWN, LEFT, RIGHT. The value for both axis will be either -1, 0 or 1.
		
		Returns:
		    Vector2D: The vector of the directional inputs
		"""
		horizontal = -1 if pygame.key.get_pressed()[self.__actions[Actions.LEFT]] else 1 * (pygame.key.get_pressed()[self.__actions[Actions.LEFT]] ^ pygame.key.get_pressed()[self.__actions[Actions.RIGHT]])

		vertical = -1 if pygame.key.get_pressed()[self.__actions[Actions.DOWN]] else 1 * (pygame.key.get_pressed()[self.__actions[Actions.DOWN]] ^ pygame.key.get_pressed()[self.__actions[Actions.UP]])

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

	def get_key_down(self, action: Enum) -> bool:
		"""Returns true during the frame the user starts pressing down the key identified by the action action enum parameter.
		
		Args:
		    action (Enum): The action that is being checked 
		
		Returns:
		    bool: Whether that action was performed that frame
		"""
		return self.__actions_performed_on_current_frame[action]


