import json
import pygame
import math
from os import path
from constants import *


        
class Chunk:
    """Provides a list of all tiles in a given chunk"""
    def __init__(self, tiles):
        self.tiles = tiles

    def __iter__(self):
        return iter(self.tiles)

    def update_chunk(self):
        # TODO add functionality for updating chunk
        pass


class Tile:
    """Provides attrbutes to uniquely identify a tile
    """
    def __init__(self, pos, custom_properties, image):
        self.x, self.y = pos
        self.image = image
        self.rect = pygame.Rect(pos, (TILE_SIZE, TILE_SIZE))
        self.collision_type = custom_properties["collision_type"]

