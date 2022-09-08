import pygame

from camera import Camera
from constants import *
from maploader import generate_map_data
from player import Player
from states import FALL


class Level:
    def __init__(self, engine, num, screen, display_surface):
        self.engine = engine
        self.num = num
        self.screen = screen
        self.display_surface = display_surface

        self.entities = []
        self.particles = []

        self.width, self.height, entities, self.chunks = generate_map_data(
            path.join(MAP_FOLDER, f"{num}.json"), CHUNK_SIZE)

        self.camera = Camera(self.width, self.height)

        for entity in entities:
            if entity["name"] == "player":
                self.player = Player(entity["x"] + 30, entity["y"] - 100, (8, 12))

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
        self.camera.update(self.player.rect)

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
        entity.grounded = False
        entity.rect.bottom += 1
        collisions = self.get_collisions(entity)
        if collisions:
            for collision in collisions:
                if entity.rect.bottom >= collision.top and entity.old_rect.bottom >= collision.top:
                    entity.rect.bottom = collision.top
                    entity.y = entity.rect.y
                    entity.velocity.y = 0
                    entity.air_timer = 0
                    entity.grounded = True
                    entity.can_jump = True

                if entity.rect.top <= collision.bottom <= entity.old_rect.top:
                    entity.rect.top = collision.bottom
                    entity.y = entity.rect.y

    def get_collisions(self, entity):
        collisions = []
        for y in range(DS_HEIGHT // (CHUNK_SIZE * TILE_SIZE)):
            for x in range(DS_WIDTH // (CHUNK_SIZE * TILE_SIZE)):
                for tile in self.chunks[(x, y)]:
                    if tile.collision_type and entity.rect.colliderect(tile.rect):
                        collisions.append(tile.rect)
        return collisions

    def draw_visible(self):
        self.display_surface.fill((0, 0, 0))
        for y in range(DS_HEIGHT // (CHUNK_SIZE * TILE_SIZE)-1):
            for x in range(DS_WIDTH // (CHUNK_SIZE * TILE_SIZE)-1):
                for tile in self.chunks[(x, y)]:
                    self.display_surface.blit(tile.image, (tile.x - self.camera.get_scroll_x(),
                                                           tile.y - self.camera.get_scroll_y()))

        for entity in self.entities:
            self.display_surface.blit(entity.image,
                                      (entity.x - self.camera.get_scroll_x(), entity.y - self.camera.get_scroll_y()))

        self.display_surface.blit(
            self.player.image, (self.player.x - self.camera.get_scroll_x(), self.player.y - self.camera.get_scroll_y()))

    def draw(self):
        self.draw_visible()
        pygame.transform.scale(self.display_surface,
                               (WIDTH, HEIGHT), dest_surface=self.screen)
        pygame.display.flip()
