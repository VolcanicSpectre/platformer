from pygame.surface import Surface

class TilesetTile:
	def __init__(self, image: Surface, collision_type):
		self.image = image
		self.collision_type = collision_type

