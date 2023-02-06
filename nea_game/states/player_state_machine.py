from nea_game.states.player_state import PlayerState


class StateMachine:
    current_state: PlayerState
    previous_state: PlayerState

    def __init__(self, starting_state: PlayerState):
        """A state machine for an entity

        Args:
            starting_state (State): The starting state for the entity
        """
        self.current_state = starting_state
        self.previous_state = starting_state

    def change_state(self, new_state: PlayerState):
        """Provides functionlaity for changing state

        Args:
            new_state (State): The new state that the entity will change to
        """
        self.current_state.exit()
        self.previous_state = self.current_state
        self.current_state = new_state
        self.current_state.enter()
