from os.path import isdir
from os import listdir
from pathlib import Path
from pygame.event import Event
from pygame.image import load
from pygame import Rect, Surface
from nea_game.calc.vector2d import Vector2D
from nea_game.components.input import Input
from nea_game.components.renderer import AnimatedRenderer
from nea_game.components.rigidbody2d import RigidBody2D
from nea_game.entity.base_entity import BaseEntity
from nea_game.ldtk_world_loader.collision_type import CollisionType
from nea_game.ldtk_world_loader.level_tile import LevelTile
from nea_game.player.sub_states.player_idle_state import PlayerIdleState
from nea_game.player.sub_states.player_in_air_state import PlayerInAirState
from nea_game.player.sub_states.player_run_state import PlayerRunState
from nea_game.player.sub_states.player_jump_state import PlayerJumpState
from nea_game.player.sub_states.player_wall_jump_state import PlayerWallJumpState
from nea_game.player.sub_states.player_slide_state import PlayerSlideState
from nea_game.player.player_action_space import PlayerActionSpace
from nea_game.states.player_state_machine import StateMachine


class Player(BaseEntity):
    frames: dict[str, list[Surface]]

    direction: int

    def __init__(
        self,
        player_folder: Path,
        level_data: list[LevelTile],
        action_bindings: list[int],
        internal_fps: int,
        x: int,
        y: int,
    ):
        """Defines player movement constants and starts the player in the idle state

        Args:
            player_folder (Path): The path to the player folder
            action_bindings (list[int]): The list of the key bindings for the player actions
            level_data (list[LevelTile]): The data of the level
            x (int): The x position of the player
            y (int): The y position of the player
        """
        super().__init__(x, y, level_data)

        self.idle_state = PlayerIdleState(self, "Idle")
        self.run_state = PlayerRunState(self, "Run")
        self.jump_state = PlayerJumpState(self, "Jump")
        self.wall_jump_state = PlayerWallJumpState(self, "WallJump")
        self.in_air_state = PlayerInAirState(self, "InAir")
        self.slide_state = PlayerSlideState(self, "Slide")
        frames = {}

        for folder in listdir(player_folder):
            if isdir(player_folder / folder):
                frames[folder] = [
                    load(player_folder / (f"{folder}/{image_name}"))
                    for image_name in listdir(player_folder / folder)
                ]

        self.renderer = AnimatedRenderer(frames)
        self.input = Input(PlayerActionSpace, action_bindings)
        self.rb = RigidBody2D(4, 0.4, internal_fps)
        self.state_machine = StateMachine(self.idle_state)

        self.direction = 1
        self.rect = Rect((self.x, self.y), self.renderer.frames["idle"][0].get_size())
        self.old_rect = self.rect

        self.x_run_speed = 1.8
        self.acceleration_rate = 3
        self.jump_hang_acceleration_mult = 2
        self.jump_hang_max_speed_mult = 1.2
        self.deceleration_rate = 10
        self.air_acceleration_multiplier = 0.6
        self.velocity_power = 0.6

        self.jump_force = 15
        self.jump_hang_time_threshold = 1.2
        self.jump_hang_gravity_mult = 0.6
        self.jump_fast_fall_mult = 1.25
        self.coyote_time = 0.1
        self.jump_buffer_time = 0.1
        self.max_fall = 3

        self.wall_jump_force = Vector2D(11, 15)
        self.wall_jump_time = 3
        self.wall_jump_lerp = 0.05

        self.wall_slide_velocity = 0.8

        self.friction = 10

    def get_collisions(self) -> list[LevelTile]:
        return [tile for tile in self.level_data if self.rect.colliderect(tile.rect)]

    @property
    def is_grounded(self) -> bool:
        for collision in [
            tile
            for tile in self.level_data
            if self.rect.move(0, 1).colliderect(tile.rect)
        ]:
            if collision.collision_type in (CollisionType.WALL, CollisionType.PLATFORM):
                if (
                    self.rect.bottom >= collision.rect.top
                    and self.old_rect.bottom <= collision.rect.top
                ):
                    return True

        return False

    @property
    def is_touching_wall(self) -> int:
        for collision in [
            tile
            for tile in self.level_data
            if self.rect.move(1, 0).colliderect(tile.rect)
        ]:
            if collision.collision_type == CollisionType.WALL:
                if (
                    self.rect.right >= collision.rect.left
                    and self.old_rect.right <= collision.rect.left
                ):
                    return 1

        for collision in [
            tile
            for tile in self.level_data
            if self.rect.move(-1, 0).colliderect(tile.rect)
        ]:
            if collision.collision_type == CollisionType.WALL:
                if (
                    self.rect.left <= collision.rect.right
                    and self.old_rect.left >= collision.rect.right
                ):
                    return -1
        return 0

    def handle_x_collisions(self):
        for collision in self.get_collisions():
            match collision.collision_type:
                case CollisionType.WALL:
                    if (
                        self.rect.right >= collision.rect.left
                        and self.old_rect.right <= collision.rect.left
                    ):
                        self.rect.right = collision.rect.left
                        self.x = self.rect.x
                        self.rb.velocity = Vector2D(0, self.rb.velocity.y)
                    if (
                        self.rect.left <= collision.rect.right
                        and self.old_rect.left >= collision.rect.right
                    ):
                        self.rect.left = collision.rect.right
                        self.x = self.rect.x
                        self.rb.velocity = Vector2D(0, self.rb.velocity.y)
                case _:
                    pass

    def handle_y_collisions(self):
        for collision in self.get_collisions():
            match collision.collision_type:
                case CollisionType.WALL:
                    if (
                        self.rect.bottom >= collision.rect.top
                        and self.old_rect.bottom <= collision.rect.top
                    ):
                        self.rect.bottom = collision.rect.top
                        self.y = self.rect.y
                        self.rb.velocity = Vector2D(self.rb.velocity.x, 0)

                    if (
                        self.rect.top <= collision.rect.bottom
                        and self.old_rect.top >= collision.rect.bottom
                    ):
                        self.rect.top = collision.rect.bottom
                        self.y = self.rect.y
                        self.rb.velocity = Vector2D(self.rb.velocity.x, 0)

                case CollisionType.PLATFORM:
                    if self.rect.top <= collision.rect.bottom <= self.old_rect.top:
                        self.rect.top = collision.rect.bottom
                        self.y = self.rect.y
                        self.rb.velocity = Vector2D(self.rb.velocity.x, 0)
                case _:
                    pass

    def event_handler(self, events: list[Event]):
        self.input.update_actions_performed_on_current_frame(events)

    def input_handler(self):
        self.state_machine.current_state.input_handler()

    def update(self, dt: float):
        if self.input.get_axis_raw().x:
            self.direction = self.input.get_axis_raw().x

        self.old_rect = self.rect.copy()
        self.input_handler()
        self.state_machine.current_state.update(dt)

        self.x += self.rb.velocity.x
        self.rect.x = int(self.x)
        self.handle_x_collisions()

        self.y += self.rb.velocity.y
        self.rect.y = int(self.y)
        self.handle_y_collisions()
