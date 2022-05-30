import pygame
from states import States


class Entity:
    def __init__(self, x, y, SIZE):
        self.state = States.IDLE

        self.SIZE = SIZE
        self.image = pygame.Surface(SIZE)
        self.image.fill("red")
        self.rect = pygame.Rect(x, y, SIZE[0], SIZE[1])
        self.old_rect = self.rect.copy()
        self.events = {"right": False, "left": False, "up": False}

        self.x, self.y = x, y

        self.velocity = pygame.Vector2(0, 0)

        self.MAXRUN = 4

        self.ACCELRUN = 0.07
        self.DECELRUN = 0.05

        self.TURNPOWER = 0.5
        self.STOPPOWER = 0.5
        self.ACCELPOWER = 0.5

        self.JUMPHEIGHT = 50
        self.JUMPDISTANCE = 50
        self.INIT_JUMP_VELOCITY = (
            (2*self.JUMPHEIGHT*self.MAXRUN) / self.JUMPDISTANCE) * -1
        self.INIT_GRAVITY = (
            (2*self.JUMPHEIGHT*self.MAXRUN**2) / self.JUMPDISTANCE**2)
        self.FINAL_GRAVITY = (
            (2*self.JUMPHEIGHT*self.MAXRUN**2) / (self.JUMPDISTANCE ** 2)*1.2)

        self.air_timer = 0

    def event_handler(self):

        new_state = self.state.handle_inputs()
        if new_state:
            self.state = new_state

    def update(self, dt):
        self.old_rect = self.rect

        self.update_x(dt)
        self.update_y(dt)

    def update_x(self, dt):
        new_state = self.state.process_x_movement(dt)
        if new_state:
            self.state = new_state

    def update_y(self, dt):
        new_state = self.state.process_y_movement(dt)
        if new_state:
            self.state = new_state

    @property
    def direction(self):
        if self.key_pressed["right"]:
            return 1
        elif self.key_pressed["left"]:
            return -1
        else:
            return 0


def load_assets():
    pass
