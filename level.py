import pygame

from collision_types import CollisionTypes
from camera import Camera
from circular_queue import CircularQueue
from constants import *
from map_loader import generate_map_data
from player import Player
from render_object import RenderObject


class Level:
    """Provides an interface to handle all logic for a level
    """

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
        """Passes down the event to the event_handler of self.player

        Args:
            event (pygame.Event):
        """
        self.player.event_handler(event)

    def global_update(self):
        """Provides an entry point to update all aspects of the level
        """
        self.update()
        self.render_visible()

    def update(self):
        """Updates all entities and the camera and handles collisions 
        """
        for entity in self.entities:
            entity.update()
            self.handle_collisions(entity)

        self.player.update(self.engine.dt)
        self.handle_collisions(self.player)
        self.camera.update(self.player.rect)

    def handle_collisions(self, entity):
        """Updates one axis of the entity and then checks for collisions on that axis. The other axis is then updated and collsions are checked.

        Args:
            entity (Entity): An entity object
        """
        entity.update_x(self.engine.dt)
        collisions = self.get_collisions(entity)
        entity.collisions = {
            CollisionTypes.X_WALL_LEFT: False, CollisionTypes.X_WALL_RIGHT: False}
        if collisions:
            for collision in collisions:
                if entity.rect.right >= collision.left >= entity.old_rect.right:
                    entity.rect.right = collision.left
                    entity.x = entity.rect.x
                    entity.collisions[CollisionTypes.X_WALL_RIGHT] = True

                if entity.rect.left <= collision.right <= entity.old_rect.left:
                    entity.rect.left = collision.right
                    entity.x = entity.rect.x
                    entity.collisions[CollisionTypes.X_WALL_LEFT] = True

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
                    entity.can_dash = not entity.is_dashing and entity.dash_cooldown_timer <= 0

                if entity.rect.top <= collision.bottom <= entity.old_rect.top:
                    entity.rect.top = collision.bottom
                    entity.velocity.y = 0
                    entity.y = entity.rect.y

    def get_visible_chunks(self):
        """Returns a list of all the chunks that are visible on the screen

        Returns:
            List[Chunk]: A list of all chunk objects that are currently visible on the display
        """
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
        """Returns a list of all collisions with a given entity

        Args:
            entity (Entity): 

        Returns:
            List[pygame.Rect]: A list of pygame.Rect objects representing all of the collsions with a given entity
        """
        collisions = []
        for chunk in self.get_visible_chunks():
            for tile in chunk:
                if tile.collision_type and entity.rect.colliderect(tile.rect):
                    collisions.append(tile.rect)
        return collisions

    def update_render_queue(self):
        """Adds all objects to be drawn this frame to the render_queue if it is visible on the screen
        """
        for chunk in self.get_visible_chunks():
            for tile in chunk:
                self.render_queue.enqueue(
                    RenderObject(tile.x, tile.y, tile.image))

        for entity in self.entities:
            self.render_queue.enqueue(RenderObject(
                entity.x, entity.y, entity.image))

        self.render_queue.enqueue(
            RenderObject(self.player.x, self.player.y, self.player.image))

    def render_visible(self):
        """Dequeues self.render_queue until render_queue.is_empty() is True and draws the render_objects onto the self.display_surface and scales them onto self.screen, self.screen is then updated
        """
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
