from constants import *


class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.true_scroll_x = 0
        self.true_scroll_y = 0
        self.scroll_x = 0
        self.scroll_y = 0

    def update(self, target_rect):
        if 0 <= self.true_scroll_x <= (self.width - DS_WIDTH + TILE_SIZE):
            self.scroll_x = int(self.true_scroll_x)

        if 0 <= self.true_scroll_y <= (self.height - DS_HEIGHT + TILE_SIZE):
            self.scroll_y = int(self.true_scroll_y)

        self.true_scroll_x += (target_rect.centerx - self.true_scroll_x - (
                DS_WIDTH - target_rect.width + TILE_SIZE) // 2) / 20
        self.true_scroll_y += (target_rect.centery - self.true_scroll_y - (
                DS_HEIGHT - target_rect.height + TILE_SIZE) // 2) / 20

    def get_scroll_x(self):
        return int(self.scroll_x)

    def get_scroll_y(self):
        return int(self.scroll_y)
