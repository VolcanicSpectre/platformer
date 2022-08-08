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
        self.ACCELAIR = 30
        self.TURNPOWER = 2
        self.STOPPOWER = 2.5
        self.ACCELPOWER = 2

        self.JUMPHEIGHT = 2.8 * TILE_SIZE
        self.JUMPDISTANCE = 4 * TILE_SIZE
        self.INIT_JUMP_VELOCITY = 2 * (
                (2 * self.JUMPHEIGHT * self.MAXRUN) / self.JUMPDISTANCE) * -1
        self.INIT_GRAVITY = 100 * (
                (self.JUMPHEIGHT * self.MAXRUN ** 2) / (2 * self.JUMPDISTANCE ** 2))
        self.FINAL_GRAVITY = 100 * (
                (self.JUMPHEIGHT * self.MAXRUN ** 2) / (self.JUMPDISTANCE ** 2))
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
        self.y += self.velocity.y * dt * TARGET_FPS
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
