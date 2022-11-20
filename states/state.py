from time import perf_counter

from entity.base_entity import BaseEntity

class State:
	def __init__(self, entity: BaseEntity, state_name: str) -> None:
		"""A template state class
		
		Args:
		    entity (BaseEntity): The entity that the state belongs to
		    state_name (str): The string representation of the state
		"""
		self.entity = entity
		self.state_name: str = state_name
		self.start_time: float

	def enter(self) -> None:
		"""Called when entering the state
		"""
		self.start_time = perf_counter()
		self.do_checks() 
	
	def exit(self) -> None:
		"""Called when leaving the state
		"""
		pass

	def update(self) -> None:
		"""Called each frame
		"""
		self.do_checks()

	def do_checks(self) -> None:
		"""Performs checks for the entity
		"""
		pass

