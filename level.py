import pygame

from camera import Camera
from constants import *
from map_loader import generate_map_data
from player import Player
from render_object import RenderObject
from queue import CircularQueue


class Level:
    def __init__(self, engine, num, screen, display_surface):
        self.engine = engine
        self.num = num
        self.screen = screen
        self.display_surface = display_surface
        self.render_queue = CircularQueue(100, RenderObject)

        self.entities = []
        self.particles = []

        self.width, self.height, entities, self.chunks = generate_map_data(
            path.join(MAP_FOLDER, f"test.json"), CHUNK_SIZE)

        self.camera = Camera(self.width, self.height)

        for entity in entities:
            if entity["name"] == "player":
                self.player = Player(entity["x"], entity["y"], (8, 12))

    def event_handler(self, event):
        self.player.event_handler(event)

    def global_update(self):
        self.update()
        self.render_visible()

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
                    entity.can_dash = not entity.is_dashing

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

    def update_render_queue(self):
        for chunk_x, chunk_y in self.chunks:
            if pygame.Rect(chunk_x * CHUNK_SIZE * TILE_SIZE, chunk_y * CHUNK_SIZE * TILE_SIZE,
                           CHUNK_SIZE * TILE_SIZE, CHUNK_SIZE * TILE_SIZE).colliderect(self.camera.true_scroll_x,
                                                                                       self.camera.true_scroll_y,
                                                                                       DS_WIDTH, DS_HEIGHT):
                for tile in self.chunks[chunk_x, chunk_y]:
                    self.render_queue.enqueue(RenderObject(tile.x, tile.y, pygame.surfarray.array2d(tile.image)))

        for entity in self.entities:
            self.render_queue.enqueue(RenderObject(entity.x, entity.y, pygame.surfarray.array2d(entity.image)))

        self.render_queue.enqueue(
            RenderObject(self.player.x, self.player.y, pygame.surfarray.array2d(self.player.image)))
        pygame.display.flip()

    def render_visible(self):
        self.update_render_queue()
        while not self.render_queue.is_empty():
            render_object = self.render_queue.dequeue()
            self.display_surface.blit(pygame.surfarray.make_surface(render_object.image),
                                      render_object.x - self.camera.get_scroll_x(),
                                      render_object.y - self.camera.get_scroll_y())
