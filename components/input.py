import pygame

class Input:
	def __init__(self, action_space: list[str], action_bindings: list[int]):
		self.actions = {action_in_space: binding for action_in_space, binding in zip(action_space, action_bindings)}

	def 