from pygame import Rect
from tileset_tile import TilesetTile

class MapTile(TilesetTile):
	def __init__(self, image, collision_type, x, y, size):
		super(MapTile, self).__init__(image, collision_type)

		self.rect = Rect(x, y, size, size)
		
