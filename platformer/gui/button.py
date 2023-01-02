from os.path import join
from pygame.image import load
from pygame.mask import from_surface

class Button:
    def __init__(self, path: str, x: int, y: int):
        self.x = x
        self.y = y

        self.passive_image = load(join(path, "0.png"))
        self.active_image = load(join(path, "1.png"))
        self.on_click_image = load(join(path, "2.png"))
        self.current_image = self.passive_image
        
        self.rect = self.passive_image.get_rect()
        self.mask = from_surface(self.passive_image)
        self.rect.topleft = self.x, self.y

    def render(self, mouse_pos: tuple[int, int]):
        mouse_pos_x, mouse_pos_y = mouse_pos

        mouse_pos_in_mask = mouse_pos_x - self.rect.x, mouse_pos_y - self.rect.y
        if self.rect.collidepoint(mouse_pos) and self.mask.get_at(mouse_pos_in_mask):
            self.current_image
