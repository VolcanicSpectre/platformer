from pygame import Rect


class Camera:
    def __init__(
        self,
        height: int,
        width: int,
        surface_height: int,
        surface_width: int,
    ):
        self.height = height
        self.width = width

        self.surface_height = surface_height
        self.surface_width = surface_width

        self.scroll_x: int = 0
        self.scroll_y: int = 0

        self.trauma: float = 0

    def update(self, target_rect: Rect):
        """Updates the scroll values of the camera to focus on the target

        Args:
            target_rect (Rect): The rect for a given target
        """

        self.scroll_x += int((target_rect.x - self.scroll_x - self.surface_width // 2) * 0.2)

        self.scroll_y += int((target_rect.centery - self.scroll_y - self.surface_height // 2) * 0.2)

    def get_scroll_x(self):
        return int(self.scroll_x)

    def get_scroll_y(self):
        return int(self.scroll_y)
