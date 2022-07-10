import pygame

from camera import Camera
from constants import *
from maploader import generate_map_data
from player import Player


class Level:
    def __init__(self, engine, num, screen, display_surface):
        self.engine = engine
        self.num = num
        self.screen = screen
        self.display_surface = display_surface

        self.entities = []
        self.particles = []

        self.width, self.height, entities, self.chunks = generate_map_data(
            path.join(MAP_FOLDER, f"n{num}.json"), CHUNK_SIZE)

        self.camera = Camera(DS_WIDTH, DS_HEIGHT)

        for entity in entities:
            if entity["name"] == "player":
                self.player = Player(entity["x"] + 8, entity["y"] - 80, (8, 12))

    def event_handler(self, event):
        self.player.event_handler(event)

    def global_update(self):
        self.update()
        self.draw()

    def update(self):
        for entity in self.entities:
            entity.update()
            self.handle_collisions(entity)

        self.player.update()
        self.handle_collisions(self.player)
        self.camera.focus(self.player)

    def handle_collisions(self, entity):
        entity.update_x(self.engine.dt)
        collisions = self.get_collisions(entity)
        if collisions:
            for collision in collisions:
                if entity.rect.right >= collision.left >= entity.old_rect.right:
                    entity.rect.right = collision.left
                    entity.x = entity.rect.x
                if entity.rect.left <= collision.right <= entity.old_rect.left:
                    entity.rect.left = collision.right
                    entity.x = entity.rect.x

        entity.update_y(self.engine.dt)
        collisions = self.get_collisions(entity)
        if collisions:
            for collision in collisions:
                if entity.rect.bottom >= collision.top and entity.old_rect.bottom >= collision.top:
                    entity.rect.bottom = collision.top
                    entity.y = entity.rect.y
                    entity.velocity.y = 0
                    entity.air_timer = 0

                if entity.rect.top <= collision.bottom <= entity.old_rect.top:
                    entity.rect.top = collision.bottom
                    entity.y = entity.rect.y

    def get_collisions(self, entity):
        collisions = []
        for y in range(5):  # 5= DS_HEIGHT/(CHUNKSIZE*TILESIZE)
            for x in range(9):  # 9= DS_WIDTH/(CHUNKSIZE*TILESIZE)
                for tile in self.chunks[(x, y)]:
                    if tile.collision_type and entity.rect.colliderect(tile.rect):
                        collisions.append(tile.rect)
        return collisions

    def draw_visible(self):
        self.display_surface.fill((0, 0, 0))
        for y in range(5):  # 6= DS_HEIGHT/(CHUNKSIZE*TILESIZE) + 1
            for x in range(9):  # 10= DS_WIDTH/(CHUNKSIZE*TILESIZE) + 1
                for tile in self.chunks[(x, y)]:
                    self.display_surface.blit(tile.image, tile.pos)

        for entity in self.entities:
            if entity.rect.contains(self.camera.rect) or entity.rect.colliderect(self.camera.rect):
                self.display_surface.blit(entity.image, (entity.x, entity.y))

        self.display_surface.blit(
            self.player.image, (self.player.x, self.player.y))

    def draw(self):
        self.draw_visible()
        pygame.transform.scale(self.display_surface,
                               (WIDTH, HEIGHT), dest_surface=self.screen)
        pygame.display.flip()
