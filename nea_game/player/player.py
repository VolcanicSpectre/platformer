import itertools
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
from nea_game.player.sub_states.player_dash_state import PlayerDashState
from nea_game.player.sub_states.player_idle_state import PlayerIdleState
from nea_game.player.sub_states.player_in_air_state import PlayerInAirState
from nea_game.player.sub_states.player_jump_state import PlayerJumpState
from nea_game.player.sub_states.player_land_state import PlayerLandState
from nea_game.player.sub_states.player_run_state import PlayerRunState
from nea_game.player.sub_states.player_slide_state import PlayerSlideState
from nea_game.player.sub_states.player_wall_jump_state import PlayerWallJumpState
from nea_game.player.player_action_space import PlayerActionSpace
from nea_game.states.player_state_machine import StateMachine


class Player(BaseEntity):
    chunks: dict[tuple[int, int], list[LevelTile]]

    idle_state: PlayerIdleState
    run_state: PlayerRunState
    land_state: PlayerLandState
    dash_state: PlayerDashState
    jump_state: PlayerJumpState
    wall_jump_state: PlayerWallJumpState
    in_air_state: PlayerInAirState
    slide_state: PlayerSlideState

    renderer: AnimatedRenderer
    input_: Input
    rigid_body: RigidBody2D
    state_machine: StateMachine

    direction: int

    rect: Rect
    old_rect: Rect

    x_run_speed: float
    acceleration_rate: float
    jump_hang_acceleration_mult: float
    jump_hang_max_speed_mult: float
    deceleration_rate: float
    air_acceleration_multiplier: float
    velocity_power: float

    jump_force: float
    jump_hang_time_threshold: float
    jump_hang_gravity_mult: float
    jump_fast_fall_mult: float
    coyote_time: float
    jump_buffer_time: float
    max_fall: float
    land_animation_time: float

    wall_jump_force: Vector2D
    wall_jump_time: float
    wall_jump_lerp: float

    wall_slide_velocity: float

    can_dash: bool
    dash_time: float
    dash_speed: float

    friction: float

    def __init__(
        self,
        player_folder: Path,
        chunks: dict[tuple[int, int], list[LevelTile]],
        action_bindings: list[int],
        internal_fps: int,
        position: tuple[int, int],
    ):
        """Defines player movement constants and starts the player in the idle state

        Args:
            player_folder (Path): The path to the player folder
            chunks (dict[tuple[int, int], list[LevelTile]]) A dictionary that stores every tile in the the level
            action_bindings (list[int]): The list of the key bindings for the player actions
            level_data (list[LevelTile]): The data of the level
            x (int): The x position of the player
            y (int): The y position of the player
        """
        super().__init__(position)
        self.chunks = chunks

        self.idle_state = PlayerIdleState(self, "Idle")
        self.run_state = PlayerRunState(self, "Run")
        self.land_state = PlayerLandState(self, "Land")
        self.dash_state = PlayerDashState(self, "Dash")
        self.jump_state = PlayerJumpState(self, "Jump")
        self.wall_jump_state = PlayerWallJumpState(self, "WallJump")
        self.in_air_state = PlayerInAirState(self, "InAir")
        self.slide_state = PlayerSlideState(self, "Slide")

        frames: dict[str, list[Surface]] = {}

        for folder in listdir(player_folder):
            if isdir(player_folder / folder):
                frames[folder] = [
                    load(player_folder / (f"{folder}/{image_name}"))
                    for image_name in listdir(player_folder / folder)
                ]

        self.renderer = AnimatedRenderer(frames)
        self.input_ = Input(PlayerActionSpace, action_bindings)
        self.rigid_body = RigidBody2D(4, 0.4, internal_fps)
        self.state_machine = StateMachine(self.idle_state)

        self.direction = 1
        self.rect = Rect(
            (self.x, self.y),
            self.renderer.frames[self.state_machine.current_state.state_name][
                0
            ].get_size(),
        )

        self.old_rect = self.rect

        self.x_run_speed = 1.6
        self.acceleration_rate = 3
        self.jump_hang_acceleration_mult = 2
        self.jump_hang_max_speed_mult = 1.2
        self.deceleration_rate = 10
        self.air_acceleration_multiplier = 0.6
        self.velocity_power = 0.6

        self.jump_force = 10
        self.jump_hang_time_threshold = 0.5
        self.jump_hang_gravity_mult = 0.6
        self.jump_fast_fall_mult = 2
        self.coyote_time = 0.1
        self.jump_buffer_time = 0.1
        self.max_fall = 3
        self.land_animation_time = 0.15

        self.wall_jump_force = Vector2D(8, 12)
        self.wall_jump_time = 3
        self.wall_jump_lerp = 0.08

        self.wall_slide_velocity = 0.74

        self.can_dash = False
        self.dash_time = 0.1
        self.dash_speed = 13
        self.friction = 10

    def get_collisions(self) -> list[LevelTile]:
        return [
            tile
            for tile in itertools.chain(*self.chunks.values())
            if self.rect.colliderect(tile.rect)
        ]

    def is_alive(self, level_height: int) -> bool:
        if self.rect.y < 0 or self.rect.y > level_height:
            return False
        for collision in self.get_collisions():
            if collision.collision_type == CollisionType.SPIKE:
                return False

        return True

    @property
    def is_grounded(self) -> bool:
        for collision in [
            tile
            for tile in itertools.chain(*self.chunks.values())
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
            for tile in itertools.chain(*self.chunks.values())
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
            for tile in itertools.chain(*self.chunks.values())
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
                        self.rigid_body.velocity = Vector2D(
                            0, self.rigid_body.velocity.y
                        )
                    if (
                        self.rect.left <= collision.rect.right
                        and self.old_rect.left >= collision.rect.right
                    ):
                        self.rect.left = collision.rect.right
                        self.x = self.rect.x
                        self.rigid_body.velocity = Vector2D(
                            0, self.rigid_body.velocity.y
                        )
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
                        self.rigid_body.velocity = Vector2D(
                            self.rigid_body.velocity.x, 0
                        )

                    if (
                        self.rect.top <= collision.rect.bottom
                        and self.old_rect.top >= collision.rect.bottom
                    ):
                        self.rect.top = collision.rect.bottom
                        self.y = self.rect.y
                        self.rigid_body.velocity = Vector2D(
                            self.rigid_body.velocity.x, 0
                        )

                case CollisionType.PLATFORM:
                    if (
                        self.rect.bottom >= collision.rect.top
                        and self.old_rect.bottom <= collision.rect.top
                    ):
                        self.rect.bottom = collision.rect.top
                        self.y = self.rect.y
                        self.rigid_body.velocity = Vector2D(
                            self.rigid_body.velocity.x, 0
                        )
                case _:
                    pass

    def event_handler(self, events: list[Event]):
        self.input_.update_actions_performed_on_current_frame(events)

    def input_handler(self):
        self.state_machine.current_state.input_handler()

    def update(self, delta_time: float):

        if self.input_.get_axis_raw().x:
            self.direction = int(self.input_.get_axis_raw().x)

        self.old_rect = self.rect.copy()
        self.input_handler()
        self.state_machine.current_state.update(delta_time)

        self.x += self.rigid_body.velocity.x
        self.rect.x = int(self.x)
        self.handle_x_collisions()

        self.y += self.rigid_body.velocity.y
        self.rect.y = int(self.y)
        self.handle_y_collisions()
