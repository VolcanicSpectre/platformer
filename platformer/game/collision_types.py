from enum import Enum, auto

class CollisionTypes:
	def __init__(self, uid: int, collision_types):
		self.uid = uid
		for collision_type in collision_types:
			exec(f"{collision_type.upper()} =  auto()")

		
