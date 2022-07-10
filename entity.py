import pygame

from states import IDLE


class Entity:
    def __init__(self, x: int, y: int, SIZE: list[int]):
        self.state = IDLE(self)

        self.SIZE = SIZE
        self.image = pygame.Surface(SIZE)
        self.image.fill("red")
        self.rect = pygame.Rect(x, y, SIZE[0], SIZE[1])
        self.old_rect = self.rect.copy()
        self.events = {"right": False, "left": False, "up": False}

        self.x, self.y = x, y

        self.velocity = pygame.Vector2(0, 0)
        self.direction = 0
        self.MAXRUN = 50
        self.ACCELRUN = 180
        self.DECELRUN = 400

        self.TURNPOWER = 2
        self.STOPPOWER = 2.5
        self.ACCELPOWER = 2

        self.JUMPHEIGHT = 50
        self.JUMPDISTANCE = 50
        self.INIT_JUMP_VELOCITY = (
                                          (2 * self.JUMPHEIGHT * self.MAXRUN) / self.JUMPDISTANCE) * -1
        self.INIT_GRAVITY = (
                (2 * self.JUMPHEIGHT * self.MAXRUN ** 2) / self.JUMPDISTANCE ** 2)
        self.FINAL_GRAVITY = (
                (2 * self.JUMPHEIGHT * self.MAXRUN ** 2) / (self.JUMPDISTANCE ** 2) * 1.2)
        self.air_timer = 0

    def update(self):
        self.old_rect = self.rect.copy()
        self.update_direction()
        self.state = self.state.input_handler()

    def update_x(self, dt):
        new_state = self.state.process_x_movement(dt)
        if new_state:
            self.state = new_state
        self.x += self.velocity.x * dt
        self.rect.x = round(self.x)

    def update_y(self, dt):
        new_state = self.state.process_y_movement(dt)
        if new_state:
            self.state = new_state
        self.y += self.velocity.y * dt
        self.rect.y = self.y

    def update_direction(self):
        if self.events["right"]:
            self.direction = 1
        elif self.events["left"]:
            self.direction = -1
        else:
            self.direction = 0


def load_assets():
    pass
