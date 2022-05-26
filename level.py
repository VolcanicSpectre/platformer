import pygame
from os import path

from constants import *
from functools import lru_cache
from maploader import generate_map_data
from camera import Camera
from player import Player


class Level:
    def __init__(self, engine, num, screen, display_surface):
        self.engine = engine
        self.num = num
        self.screen = screen
        self.display_surface = display_surface
        
        self.entities = []
        self.particles = []

        self.width, self.height, entities, self.chunks = generate_map_data(path.join(MAP_FOLDER, f"n{num}.json"), CHUNK_SIZE)

        self.camera = Camera(DS_WIDTH, DS_HEIGHT)
        
        for entity in entities:
            if entity["name"] == "player":
                self.player = Player(entity["x"], entity["y"], (8,8))
    
    def event_handler(self, event):
        pass
    
    def global_update(self):
        self.update()
        self.draw()
    
    def update(self):
        pass

    def handle_collisions(self, entity):
        collisions = self.get_collisions(entity)

    def get_collisions(self, entity):
        collisions = []
        for y in range(5): # 5= DS_HEIGHT/(CHUNKSIZE*TILESIZE)
            for x in range(9): # 19= DS_WIDTH/(CHUNKSIZE*TILESIZE)
                target_x = x + int(self.camera.rect.x/(CHUNK_SIZE*16))
                target_y = y + int(self.camera.rect.y/(CHUNK_SIZE*16))
                
            
                for tile in self.chunks[(target_x, target_y)]:
                    if tile.collision_type and entity.rect.colliderect(tile.rect):
                        collisions.append(tile.rect)
                 
    @lru_cache(maxsize=10)
    def draw_visible_chunks(self):
        for y in range(5): # 6= DS_HEIGHT/(CHUNKSIZE*TILESIZE) + 1
            for x in range(9): # 10= DS_WIDTH/(CHUNKSIZE*TILESIZE) + 1
                target_x = x + int(self.camera.rect.x/(CHUNK_SIZE*16))
                target_y = y + int(self.camera.rect.y/(CHUNK_SIZE*16))
                
                for tile in self.chunks[(target_x, target_y)]:
                    self.display_surface.blit(tile.image, tile.pos)

    def draw(self):
        self.draw_visible_chunks()
        pygame.transform.scale(self.display_surface, (1152, 640), dest_surface=self.screen)
        pygame.display.flip()