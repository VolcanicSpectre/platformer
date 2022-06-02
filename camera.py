from pygame import Rect
from constants import *


class Camera:
    def __init__(self, width, height):
        self.rect = Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def focus(self, target):
        x = (target.x - self.rect.x - (DS_WIDTH // 2) - target.rect.w // 2) / 10
        y = target.rect.y - self.rect.y - (DS_HEIGHT // 2) - target.rect.h // 2

        self.rect.x += x
        self.rect.x = min(max(0, self.rect.x), DS_WIDTH+self.width)
        self.rect.y += y
        self.rect.y = min(max(0, self.rect.y), DS_HEIGHT-self.height)
