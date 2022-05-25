from os import path

from constants import *

from maploader import generate_map_data
from camera import Camera
from player import Player


class Level:
    def __init__(self, engine, num):
        self.engine = engine
        self.num = num
        self.entities = []
        self.particles = []

        self.width, self.height, entities, self.chunks = generate_map_data(path.join(MAP_FOLDER, f"n{num}.json"), CHUNK_SIZE)

        self.camera = Camera(DS_WIDTH, DS_HEIGHT)
        
        for entity in entities:
            if entity["name"] == "player":
                self.player = Player([entity["x"], entity["y"]])
    
    def global_update(self):
        self.update()
        self.draw()
    
    def update(self):
        pass
    

    def get_visible_chunks(self):
        chunk_keys = []
        for y in range(6): # 6= DS_HEIGHT/(CHUNKSIZE*TILESIZE) + 1
            for x in range(10): # 10= DS_WIDTH/(CHUNKSIZE*TILESIZE) + 1
                target_x = x + int(self.camera.rect.x/(CHUNK_SIZE*16))
                target_y = y + int(self.camera.rect.y/(CHUNK_SIZE*16))
                chunk_keys.append((target_x, target_y))
        
        return chunk_keys

    def draw(self):
        pass