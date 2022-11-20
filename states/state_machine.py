from state import State

class StateMachine:
	def __init__(self, starting_state: State) -> None:
		"""A template for state machine for an entity
		
		Args:
		    starting_state (State): The starting state for the entity
		"""
		self.__current_state = starting_state

	def change_state(self, new_state: State) -> None:
		"""Provides functionlaity for changing state
		
		Args:
		    new_state (State): The new state that the entity will change to
		"""
		self.__current_state.exit()
		self.__current_state = new_state
		self.__current_state.enter()
		
	def get_current_state(self) -> State:
		"""A getter for current_state
		
		Returns:
		    State: The current state of the entity
		"""
		return self.__current_state

