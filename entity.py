import pygame

from constants import *
from states import IDLE
from collision_types import CollisionTypes
from agent import Agent

class Entity:
    def __init__(self, x: int, y: int, size: tuple[int, int], use_ai=False):
        self.use_ai = True
        if self.use_ai:
            self.agent = Agent()
            self.agent.build_network()
        self.state = IDLE(self)
        self.SIZE = size
        self.image = pygame.Surface(size)
        self.image.fill("red")
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.old_rect = self.rect.copy()
        self.events = {"right": False, "left": False, "up": False, "down": False, "dash": False}
        self.collisions = {CollisionTypes.X_WALL_LEFT: False, CollisionTypes.X_WALL_RIGHT: False}
        self.direction = pygame.math.Vector2(0, 0)
        self.x, self.y = x, y

        self.velocity = pygame.Vector2(0, 0)

        self.MAX_RUN = 1.25
        self.ACCEL_RUN = 150
        self.DECEL_RUN = 250
        self.ACCEL_AIR = 36
        self.TURN_POWER = 2
        self.STOP_POWER = 2.5
        self.ACCEL_POWER = 2
        self.RUN_REDUCE = 1
        self.AIR_REDUCE = 0.8

        self.JUMP_HEIGHT = 3.2 * TILE_SIZE
        self.TIME_TO_JUMP_PEAK = 0.3
        self.JUMP_GRACE_TIME = 0.05

        self.GRAVITY = (2 * self.JUMP_HEIGHT) / (pow(self.TIME_TO_JUMP_PEAK, 2))
        self.MAX_FALL = self.GRAVITY / 5
        self.INIT_JUMP_VELOCITY = self.GRAVITY * self.TIME_TO_JUMP_PEAK * -1
        self.air_timer = 0
        self.grounded = False
        self.can_jump = True

        self.can_dash = False
        self.is_dashing = False
        self.dash_cooldown_timer = 0

        self.DASH_POWER = 4
        self.DASH_ACCEL = 400
        self.Y_AXIS_MULT = 1.5
        self.DASH_DURATION = 0.15
        self.MIN_DASH_DURATION = 0.1
        self.DASH_COOLDOWN = 0.3

        self.SLIDE_MULT = 0.8
        self.MIN_WALL_JUMP_TIME = 0.1
        self.WALL_JUMP_TIME = 0.2
        self.WALL_JUMP_MULT = 0.18
        self.WALL_JUMP_ACCEL_MULT = 0.96
        self.can_wall_jump = False

    def update(self, dt):
        """Calls the relevant update functions to update the entity 

        Args:
            dt (float): the time between the previous and current frame
        """
        self.old_rect = self.rect.copy()
        self.update_dash_cooldown(dt)
        self.update_direction()
        self.state = self.state.input_handler()

    def update_x(self, dt):
        """Updates the x axis the entities velocity and position on the x axis

        Args:
            dt (float): the time between the previous and current frame
        """
        new_state = self.state.process_x_movement(dt)
        if new_state:
            self.state = new_state
        self.x += self.velocity.x * dt * TARGET_FPS
        self.rect.x = round(self.x)

    def update_y(self, dt):
        """Updates the y axis the entities velocity and position on the y axis

        Args:
            dt (float): the time between the previous and current frame
        """
        new_state = self.state.process_y_movement(dt)
        if new_state:
            self.state = new_state
        self.y += self.velocity.y * dt
        self.rect.y = round(self.y)

    def update_direction(self):
        """
        Updates the entities direction vector according to the relevant inputs on that frame
        """
        if self.events["right"]:
            self.direction.x = 1
        elif self.events["left"]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if self.events["up"]:
            self.direction.y = -1
        else:
            self.direction.y = 0

    def update_dash_cooldown(self, dt):
        """_summary_

        Args:
            dt (float_): the time between the previous and current frame
        """
        self.dash_cooldown_timer -= dt
        self.dash_cooldown_timer = max(0, self.dash_cooldown_timer)


def load_assets():
    pass
