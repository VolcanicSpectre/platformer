from entity_layer import EntityLayer
from platformer.game.constants import *
from tile_layer import TileLayer

class Level:
	def __init__(self, data):
		self.data = data
		self.identifer = self.data["identifer"]

		self.px_height = self.data["pxHei"]
		self.px_width = self.data["pxWid"]

		self.x = self.data["worldX"]
		self.y = self.data["worldY"]

		self.entity_layer = EntityLayer(layer_instance for layer_instance in self.data["layerInstances"] if layer_instance["__identifier"] == "Entities")
		self.tile_layer = TileLayer(layer_instance for layer_instance in self.data["layerInstances"] if layer_instance["__identifier"] == "Tiles")

