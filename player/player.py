from states.state_machine import StateMachine

class Player:
	def __init__(self):
		self.state_machine = StateMachine(states.Idle)
		