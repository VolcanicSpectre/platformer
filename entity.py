import pygame

from constants import *
from states import IDLE


class Entity:
    def __init__(self, x: int, y: int, size: tuple[int, int]):
        self.state = IDLE(self)
        self.y_heights = []
        self.SIZE = size
        self.image = pygame.Surface(size)
        self.image.fill("red")
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.old_rect = self.rect.copy()
        self.events = {"right": False, "left": False, "up": False}

        self.x, self.y = x, y

        self.velocity = pygame.Vector2(0, 0)
        self.direction = 0
        self.MAXRUN = 2.5
        self.ACCELRUN = 300
        self.DECELRUN = 500
        self.ACCELAIR = 25
        self.TURNPOWER = 2
        self.STOPPOWER = 2.5
        self.ACCELPOWER = 2

        self.JUMPHEIGHT = 2.5 * TILE_SIZE
        self.TIME_TO_JUMP_PEAK = 0.2

        self.GRAVITY = (2 * self.JUMPHEIGHT) / (pow(self.TIME_TO_JUMP_PEAK, 2))
        self.INIT_JUMP_VELOCITY = self.GRAVITY * self.TIME_TO_JUMP_PEAK * -1
        print(self.GRAVITY)
        self.MAXFALL = self.GRAVITY / 5
        self.air_timer = 0
        self.grounded = False

    def update(self):
        self.old_rect = self.rect.copy()
        self.update_direction()
        self.state = self.state.input_handler()

    def update_x(self, dt):
        new_state = self.state.process_x_movement(dt)
        if new_state:
            self.state = new_state
        self.x += self.velocity.x * dt * TARGET_FPS
        self.rect.x = round(self.x)

    def update_y(self, dt):
        new_state = self.state.process_y_movement(dt)
        if new_state:
            self.state = new_state
        self.y += self.velocity.y * dt
        self.rect.y = round(self.y)
        self.y_heights.append(self.rect.y)

    def update_direction(self):
        if self.events["right"]:
            self.direction = 1
        elif self.events["left"]:
            self.direction = -1
        else:
            self.direction = 0


def load_assets():
    pass
