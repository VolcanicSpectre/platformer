import pygame

from collision_types import CollisionTypes
from camera import Camera
from circular_queue import CircularQueue
from constants import *
from map_loader import generate_map_data
from player import Player
from render_object import RenderObject


class Level:
    def __init__(self, engine, num, screen, display_surface):
        self.engine = engine
        self.num = num
        self.screen = screen
        self.display_surface = display_surface
        self.render_queue = CircularQueue(300, RenderObject)

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

        self.player.update(self.engine.dt)
        self.handle_collisions(self.player)
        self.camera.update(self.player.rect)

    def handle_collisions(self, entity):
        entity.update_x(self.engine.dt)
        collisions = self.get_collisions(entity)
        entity.collisions = {CollisionTypes.X_WALL: False}
        if collisions:
            for collision in collisions:
                if entity.rect.right >= collision.left >= entity.old_rect.right:
                    entity.rect.right = collision.left
                    entity.x = entity.rect.x
                    entity.collisions[CollisionTypes.X_WALL] = True

                if entity.rect.left <= collision.right <= entity.old_rect.left:
                    entity.rect.left = collision.right
                    entity.x = entity.rect.x
                    entity.collisions[CollisionTypes.X_WALL] = True

        entity.update_y(self.engine.dt)
        entity.grounded = False
        entity.rect.bottom += 1
        collisions = self.get_collisions(entity)
        if collisions:
            for collision in collisions:
                if entity.rect.bottom >= collision.top >= entity.old_rect.bottom:
                    entity.rect.bottom = collision.top
                    entity.y = entity.rect.y
                    entity.velocity.y = 0
                    entity.air_timer = 0
                    entity.grounded = True
                    entity.can_jump = True
                    entity.can_dash = not entity.is_dashing and entity.dash_cooldown_timer <= 0

                if entity.rect.top <= collision.bottom <= entity.old_rect.top:
                    entity.rect.top = collision.bottom
                    entity.velocity.y = 0
                    entity.y = entity.rect.y

    def get_visible_chunks(self):
        visible_chunks = []
        for chunk_x, chunk_y in self.chunks:
            if pygame.Rect(chunk_x * CHUNK_SIZE * TILE_SIZE, chunk_y * CHUNK_SIZE * TILE_SIZE,
                           CHUNK_SIZE * TILE_SIZE, CHUNK_SIZE * TILE_SIZE).colliderect(self.camera.get_scroll_x(),
                                                                                       self.camera.get_scroll_y(),
                                                                                       DS_WIDTH,
                                                                                       DS_HEIGHT):
                visible_chunks.append(self.chunks[(chunk_x, chunk_y)])
        return visible_chunks

    def get_collisions(self, entity):
        collisions = []
        for chunk in self.get_visible_chunks():
            for tile in chunk:
                if tile.collision_type and entity.rect.colliderect(tile.rect):
                    collisions.append(tile.rect)
        return collisions

    def update_render_queue(self):
        for chunk in self.get_visible_chunks():
            for tile in chunk:
                self.render_queue.enqueue(RenderObject(tile.x, tile.y, tile.image))

        for entity in self.entities:
            self.render_queue.enqueue(RenderObject(entity.x, entity.y, entity.image))

        self.render_queue.enqueue(
            RenderObject(self.player.x, self.player.y, self.player.image))

    def render_visible(self):
        self.display_surface.fill((0, 0, 0))
        self.update_render_queue()
        while not self.render_queue.is_empty():
            render_object = self.render_queue.dequeue()
            self.display_surface.blit(render_object.image,
                                      (render_object.x - self.camera.get_scroll_x(),
                                       render_object.y - self.camera.get_scroll_y() + TILE_SIZE),
                                      )
        pygame.transform.scale(self.display_surface,
                               (WIDTH, HEIGHT), dest_surface=self.screen)
        pygame.display.flip()
